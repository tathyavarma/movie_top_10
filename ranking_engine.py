import logging
import re
from typing import Dict, List, Optional
import numpy as np
from rapidfuzz import fuzz
from config import (
    FUZZY_MATCH_THRESHOLD,
    RANKING_WEIGHTS,
)
from models.movie import Movie


class RankingEngine:
    def __init__(
        self,
        weights: Optional[Dict[str, float]] = None
    ):
        self.weights = weights or RANKING_WEIGHTS
        self.logger = logging.getLogger(
            self.__class__.__name__
        )

    def normalize_title(self, title: str) -> str:
        title = title.lower().strip()

        title = re.sub(
            r"[^a-z0-9 ]",
            "",
            title
        )

        parts = title.split()

        if parts and parts[0] == "the":
            title = " ".join(parts[1:]) + ", the"

        return title

    def merge_movies(
        self,
        movie_list: List[Movie]
    ) -> List[Movie]:

        merged: List[Movie] = []

        self.logger.info(
            f"Deduplicating {len(movie_list)} candidates..."
        )

        for candidate in movie_list:

            if not candidate.title:
                continue

            candidate_norm = self.normalize_title(
                candidate.title
            )

            matched = False

            for existing in merged:

                existing_norm = self.normalize_title(
                    existing.title
                )

                same_year = (
                    abs(existing.year - candidate.year)
                    <= 1
                )

                similarity = fuzz.ratio(
                    candidate_norm,
                    existing_norm
                )

                if (
                    same_year
                    and similarity
                    >= FUZZY_MATCH_THRESHOLD
                ):
                    self._merge_into(
                        existing,
                        candidate
                    )

                    matched = True
                    break

            if not matched:
                merged.append(candidate)

        self.logger.info(
            f"Deduplication complete: "
            f"{len(merged)} unique movies."
        )

        return merged

    def _merge_into(
        self,
        target: Movie,
        source: Movie
    ):

        simple_fields = [
            "original_title",
            "runtime",
            "director",
            "country",
            "language",
            "budget",
            "revenue",
        ]

        for field in simple_fields:
            if not getattr(target, field):
                setattr(
                    target,
                    field,
                    getattr(source, field)
                )

        list_fields = [
            "genres",
            "writers",
            "main_cast",
        ]

        for field in list_fields:
            if (
                getattr(source, field)
                and not getattr(target, field)
            ):
                setattr(
                    target,
                    field,
                    getattr(source, field)
                )

        self._merge_rating(
            target,
            source,
            "imdb_rating"
        )

        self._merge_rating(
            target,
            source,
            "tmdb_rating"
        )

        self._merge_rating(
            target,
            source,
            "rotten_critics"
        )

        self._merge_rating(
            target,
            source,
            "rotten_audience"
        )

        self._merge_rating(
            target,
            source,
            "metacritic"
        )

        if (
            not target.imdb_votes
            and source.imdb_votes
        ):
            target.imdb_votes = source.imdb_votes

        if (
            not target.num_reviews
            and source.num_reviews
        ):
            target.num_reviews = source.num_reviews

        target.award_wins += source.award_wins
        target.award_nominations += (
            source.award_nominations
        )

        if (
            source.plot
            and (
                not target.plot
                or len(source.plot)
                > len(target.plot)
            )
        ):
            target.plot = source.plot

        target.source_urls.extend(
            source.source_urls
        )

        target.source_urls = list(
            set(target.source_urls)
        )

    @staticmethod
    def _merge_rating(
        target: Movie,
        source: Movie,
        attribute: str
    ):

        source_value = getattr(
            source,
            attribute
        )

        if source_value is None:
            return

        current_value = getattr(
            target,
            attribute
        )

        if (
            current_value is None
            or source_value > current_value
        ):
            setattr(
                target,
                attribute,
                source_value
            )

    def compute_scores(
        self,
        movies: List[Movie]
    ) -> List[Movie]:

        if not movies:
            return []

        imdb_ratings = np.array(
            [m.imdb_rating for m in movies],
            dtype=float
        )

        tmdb_ratings = np.array(
            [m.tmdb_rating for m in movies],
            dtype=float
        )

        rotten_critics = np.array(
            [m.rotten_critics for m in movies],
            dtype=float
        )

        rotten_audience = np.array(
            [m.rotten_audience for m in movies],
            dtype=float
        )

        metascores = np.array(
            [m.metacritic for m in movies],
            dtype=float
        )

        imdb_votes = np.array(
            [m.imdb_votes for m in movies],
            dtype=float
        )

        review_counts = np.array(
            [m.num_reviews for m in movies],
            dtype=float
        )

        wins = np.array(
            [m.award_wins for m in movies],
            dtype=float
        )

        nominations = np.array(
            [m.award_nominations for m in movies],
            dtype=float
        )

        award_raw = (
            wins * 2 + nominations
        )

        if award_raw.max() > 0:
            award_score = (
                award_raw / award_raw.max()
            ) * 100

        else:
            award_score = np.zeros_like(
                award_raw
            )

        safe_votes = np.where(
            np.isnan(imdb_votes),
            0,
            imdb_votes
        )

        log_votes = np.log1p(safe_votes)

        if log_votes.max() > 0:
            popularity_score = (
                log_votes / log_votes.max()
            ) * 100

        else:
            popularity_score = np.zeros_like(
                log_votes
            )

        safe_reviews = np.where(
            np.isnan(review_counts),
            0,
            review_counts
        )

        log_reviews = np.log1p(
            safe_reviews
        )

        if log_reviews.max() > 0:
            review_volume = (
                log_reviews
                / log_reviews.max()
            ) * 100

        else:
            review_volume = np.zeros_like(
                log_reviews
            )

        metric_arrays = [
            imdb_ratings,
            tmdb_ratings,
            rotten_critics,
            rotten_audience,
            metascores,
        ]

        for array in metric_arrays:
            array[np.isnan(array)] = 0

        weights = self.weights

        final_scores = (
            weights["imdb_rating"]
            * imdb_ratings
            + weights["rotten_critics"]
            * rotten_critics
            + weights["metacritic"]
            * metascores
            + weights["tmdb_rating"]
            * tmdb_ratings
            + weights["awards"]
            * award_score
            + weights["popularity"]
            * popularity_score
            + weights["review_volume"]
            * review_volume
        )

        for index, movie in enumerate(movies):

            movie.final_score = round(
                float(final_scores[index]),
                2
            )

            movie.popularity_score = round(
                float(popularity_score[index]),
                2
            )

            critic_values = [
                rotten_critics[index],
                metascores[index],
            ]

            critic_filtered = [
                value
                for value in critic_values
                if value > 0
            ]

            movie.critic_consensus = round(
                float(np.mean(critic_filtered))
                if critic_filtered
                else 0,
                2
            )

            audience_values = [
                imdb_ratings[index],
                rotten_audience[index],
                tmdb_ratings[index],
            ]

            audience_filtered = [
                value
                for value in audience_values
                if value > 0
            ]

            movie.audience_consensus = round(
                float(np.mean(audience_filtered))
                if audience_filtered
                else 0,
                2
            )

            movie.cultural_impact_score = round(
                float(
                    (
                        award_score[index]
                        * 0.5
                    )
                    + (
                        popularity_score[index]
                        * 0.5
                    )
                ),
                2
            )

        movies.sort(
            key=lambda movie: movie.final_score,
            reverse=True
        )

        return movies