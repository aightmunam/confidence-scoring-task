"""
Code to run the scorer and write the confidence scores
"""
import logging
import sys

from confidence import ConfidenceScore


def setup_logger():
    """
    Setup logger to show display different logging information
    """
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.DEBUG,
        format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
    )


if __name__ == "__main__":
    setup_logger()
    confidence_scorer = ConfidenceScore(
        google_file='input/google_poi.csv',
        osm_file='input/osm_poi.csv',
        matching_file='input/google_osm_poi_matching.csv'
    )
    confidence_scorer.generate_scores_to_file()
