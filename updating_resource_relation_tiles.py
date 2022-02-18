"""
ARCHES - a program developed to inventory and manage immovable cultural heritage.
Copyright (C) 2013 J. Paul Getty Trust and World Monuments Fund
​
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.
​
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.
​
You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""
​
from django.core.management.base import BaseCommand
from arches.app.models.tile import Tile
​
​
class Command(BaseCommand):
    """
    Command for repairing invalid resource instance data
​
    """
​
    def add_arguments(self, parser):
        parser.add_argument("operation", nargs="?")
​
    def handle(self, *args, **options):
        self.update_tiles()
​
    def update_tiles(self):
​
        ## testing data for Cyrus
        # nodeinfo = [{
        #         "nodegroup":"2174dd12-17d5-11eb-98cd-acde48001122",
        #         "cardname":"place",
        #         "node":"2174dd12-17d5-11eb-98cd-acde48001122"
        #     }]
​
        nodeinfo = [{
                    "nodegroup":"34cfea2e-c2c0-11ea-9026-02e7594ce0a0",
                    "cardname":"people",
                    "node":"34cfea8a-c2c0-11ea-9026-02e7594ce0a0"
                }, 
                {
                    "nodegroup":"34cfe9b6-c2c0-11ea-9026-02e7594ce0a0",
                    "cardname":"gridid",
                    "node":"34cfea5d-c2c0-11ea-9026-02e7594ce0a0"
                }
            ]
​
        for item in nodeinfo:
            nodegroupid = item["nodegroup"]
            nodeid = item["node"]
            tiles = Tile.objects.filter(nodegroup_id = nodegroupid)  
            for tile in tiles[0:1]: # only operate on first tile
            
                val = tile.data
                try:
                    val[nodeid].keys()
                    val[nodeid] = [val[nodeid]]
                    tile.data = val
                    tile.save()
                    print('updated tile:', tile.tileid)
                    print('updated resourceid:', tile.resourceinstance_id)
                except (KeyError, AttributeError, TypeError): #skip if the data is already a list or the nodeid is not on the tile
                    pass