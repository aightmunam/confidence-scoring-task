"""
Code to calculate and store the confidence score
"""
import logging

from haversine import haversine

from utils import get_data_from_file, sigmoid, write_data_to_file

log = logging.getLogger(__name__)


class ConfidenceScore:
    """
    Load all the POI data from files and calculate confidence scores
    """

    google_poi = {}
    osm_poi = {}
    poi_matching = {}

    def __init__(self, google_file, osm_file, matching_file):
        """
        Check if all the files are provided and
        """
        if google_file and osm_file and matching_file:
            self.parse_poi_files(google_file, osm_file, matching_file)

    def parse_poi_files(self, google_file, osm_file, matching_file):
        """
        Load all the data for different poi files
        """
        self.google_poi = get_data_from_file(google_file, 'internal_id')
        self.osm_poi = get_data_from_file(osm_file, 'osm_id')
        self.poi_matching = get_data_from_file(matching_file, 'osm_id')

    def calculate_scores_for_poi(self):
        """
        Calculate scores for all the POIs by comparing google poi data and the osm poi data and
        add the scores in the poi_matching object
        """
        for poi_data in self.poi_matching.values():
            google_internal_id = poi_data['internal_id']
            google_poi_data_for_current = self.google_poi.get(google_internal_id)

            osm_id = poi_data['osm_id']
            osm_poi_data_for_current = self.osm_poi.get(osm_id)

            osm_coords = (
                float(osm_poi_data_for_current['latitude']),
                float(osm_poi_data_for_current['longitude'])
            )
            google_coords = (
                float(google_poi_data_for_current['latitude']),
                float(google_poi_data_for_current['longitude'])
            )

            distance = haversine(osm_coords, google_coords, unit='mi')
            poi_data['score'] = sigmoid(distance)

    def generate_scores_to_file(self, fields=None):
        """
        Generate the confidence scores for the POIs and writes the results to a file
        """
        if self.google_poi and self.osm_poi and self.poi_matching:
            self.calculate_scores_for_poi()
            if not fields:
                fields = ['osm_type', 'osm_id', 'internal_id', 'query', 'score']
            write_data_to_file(self.poi_matching.values(), fields)
