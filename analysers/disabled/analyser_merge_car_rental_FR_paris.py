#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2014-2016                                 ##
##                                                                       ##
## This program is free software: you can redistribute it and/or modify  ##
## it under the terms of the GNU General Public License as published by  ##
## the Free Software Foundation, either version 3 of the License, or     ##
## (at your option) any later version.                                   ##
##                                                                       ##
## This program is distributed in the hope that it will be useful,       ##
## but WITHOUT ANY WARRANTY; without even the implied warranty of        ##
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         ##
## GNU General Public License for more details.                          ##
##                                                                       ##
## You should have received a copy of the GNU General Public License     ##
## along with this program.  If not, see <http://www.gnu.org/licenses/>. ##
##                                                                       ##
###########################################################################

from modules.OsmoseTranslation import T_
from .Analyser_Merge import Analyser_Merge, SourceOpenDataSoft, CSV, Load, Conflate, Select, Mapping


class Analyser_Merge_Car_Rental_FR_Paris(Analyser_Merge):
    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        self.missing_official = self.def_class(item = 8160, id = 1, level = 3, tags = ['merge', 'public equipment'],
            title = T_('Paris Autolib\' car rental not integrated'))
        self.missing_osm = self.def_class(item = 7140, id = 2, level = 3, tags = ['merge', 'public equipment'],
            title = T_('Paris Autolib\' car rental without ref:FR:Paris:DSP'))
        self.possible_merge = self.def_class(item = 8161, id = 3, level = 3, tags = ['merge', 'public equipment'],
            title = T_('Paris Autolib\' car rental integration suggestion'))
        self.update_official = self.def_class(item = 8162, id = 4, level = 3, tags = ['merge', 'public equipment'],
            title = T_('Paris Autolib\' car rental update'))

        self.init(
            "http://opendata.paris.fr/explore/dataset/stations_et_espaces_autolib_de_la_metropole_parisienne",
            "Stations et espaces AutoLib de la métropole parisienne",
            CSV(SourceOpenDataSoft(
                attribution="Mairie de Paris",
                base_url="http://opendata.paris.fr",
                dataset="stations_et_espaces_autolib_de_la_metropole_parisienne"))
            Load("XY", "XY",
                xFunction = lambda x: x and x.split(',')[1],
                yFunction = lambda y: y and y.split(',')[0]),
            Conflate(
                select = Select(
                    types = ["ways",  "nodes"],
                    tags = {"amenity": "car_rental", "network": "Autolib'"}),
                osmRef = "ref:FR:Paris:DSP",
                conflationDistance = 200,
                mapping = Mapping(
                    static1 = {
                        "amenity": "car_rental",
                        "network": "Autolib'",
                        "operator": "Autolib'"},
                    static2 = {"source": self.source},
                    mapping1 = {
                        "name": "ID Autolib",
                        "ref:FR:Paris:DSP": "ID DSP",
                        "capacity": lambda res: int(float(res["prises Autolib"]))} )))
