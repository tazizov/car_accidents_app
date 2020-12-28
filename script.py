import geopandas as gpd
import json
import pandas as pd
from shapely.geometry import Point
import numpy as np
from multiprocessing import Pool
import os
from tqdm import tqdm

global_dict = {}


def get_min_ind(point):
    ind_min = global_dict['roads_geometry'].apply(lambda road: road.distance(point)).argmin()
    ind = global_dict['roads_ids'][ind_min]
    return ind


def init_worker(roads_ids, roads_geometry):
    global_dict['roads_ids'] = roads_ids
    global_dict['roads_geometry'] = roads_geometry


def run_in_parallel(points, roads_ids, roads_geometry, line_ids):
    with Pool(os.cpu_count() - 1, initializer=init_worker, initargs=(roads_ids, roads_geometry)) as pool:
        jobs = [pool.apply_async(get_min_ind, (point,)) for point in points.geom]

        for i, job in tqdm(enumerate(jobs)):
            line_ids[i] = job.get()
            if i % 2000 == 0:
                points['road_id'] = line_ids
                points.to_pickle('./data/preprocessed/points_with_roads.pkl')

        points['road_id'] = line_ids
        points.to_pickle('./data/preprocessed/points_with_roads.pkl')

        pool.close()
        pool.join()


def get_line_ids():
    roads = gpd.read_file(json.load(open('data/london_roads.json')))
    roads_ids = roads.id.values
    points = pd.read_pickle('./data/preprocessed/accidents_with_score.pkl')
    points['geom'] = points.apply(lambda x: Point(x['Longitude'], x['Latitude']), axis=1)
    line_ids = np.zeros(len(points))
    run_in_parallel(points, roads_ids, roads.geometry, line_ids)


if __name__ == '__main__':
    get_line_ids()
