#!/opt/intel/oneapi/intelpython/latest/bin/python

from lxml import html
#from mechanize import Browser
from bs4 import BeautifulSoup
import requests
from time import sleep
from tqdm import tqdm
import sys
import numpy as np
import pandas as pd
from recent_stats import scrape_new
from mlp import run_mlp 

default_DIR = '/home/khermans/code/bts/'

def main():

    outfile = '/home/khermans/OneDrive/bts/scrape.csv'
    filename = scrape_new()
    run_mlp(filename, outfile)

    return

if __name__ == "__main__":
    main()
