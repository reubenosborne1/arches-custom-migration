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
from django.core.management.base import BaseCommand
from arches.app.models.tile import Tile
class Command(BaseCommand):
	"""
	Command for repairing invalid resource instance data
​
	"""
	def add_arguments(self, parser):
		parser.add_argument("operation", nargs="?")
	def handle(self, *args, **options):
		self.update_tiles()
	def update_tiles(self):
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
		for item in nodeinfo:
			print(f'Starting {item["cardname"]}...')
			nodegroupid = item["nodegroup"]
			nodeid = item["node"]
			tiles = Tile.objects.filter(nodegroup_id = nodegroupid)
			print(f'Total tiles:{len(tiles)}')  
			for i,tile in enumerate(tiles[0:1000]): # only operate on first tile
				val = tile.data
				# if the nodeid not in tile data
				if val[nodeid] is None:
					print(val)
				# 	val[nodeid] = None
				# 	tile.data = val
				# 	tile.save() 
				# 	print('updated tile:', tile.tileid)
				# 	print('updated resourceid:', tile.resourceinstance_id)
				# if i % 1000 == 0:
				# 	print(f'{i} tiles complete')
				# # except (KeyError, AttributeError, TypeError): #skip if the data is already a list or the nodeid is not on the tile
				# # 	pass