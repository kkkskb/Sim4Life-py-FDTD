from __future__ import absolute_import
from __future__ import print_function
import sys, os
import numpy as np

import s4l_v1.document as document
import s4l_v1.model as model
import s4l_v1.simulation.emfdtd as fdtd
import s4l_v1.analysis as analysis
import s4l_v1.analysis.viewers as viewers
import s4l_v1.materials.database as database # <-- 追加: 材料データベースのインポート

import s4l_v1.units as units

_CFILE = os.path.abspath(sys.argv[0] if __name__ == '__main__' else __file__ )
_CDIR = os.path.dirname(_CFILE)

def CreateModel():
	from s4l_v1.model import Vec3

	wire = model.CreateWireBlock(p0=Vec3(0,0,0), p1=Vec3(100, 100, 100), parametrized=True)
	block1 = model.CreateSolidBlock(p0=Vec3(10,10,10), p1=Vec3(90, 90, 90), parametrized=True)
	block1.Name = 'Muscle Block'  # モデルブロックの名前を変更

	wire.Name = 'Plane Wave Source'

def CreateSimulation():

	# retrieve needed entities from model
	entities = model.AllEntities()

	entity__wire_block1 = entities['Plane Wave Source']
	entity__tissue = entities['Muscle Block']  # モデルブロックを取得

	sim = fdtd.Simulation()

	sim.Name = 'Plane Wave Simulation'

	# Setup
	sim.SetupSettings.SimulationTime = 10., units.Periods

	# Materials:
	# Adding a new MaterialSettings for Muscle
	material_settings_muscle = fdtd.MaterialSettings()
	components_muscle = [entity__tissue]  # ワイヤブロックをターゲットにする
	mat_muscle = database["IT'IS 4.1"]["Muscle"]
	if mat_muscle is not None:
		sim.LinkMaterialWithDatabase(material_settings_muscle, mat_muscle)
	else:
		print("Warning: 'Muscle' material not found in database. Using fallback values.")
		material_settings_muscle.Name = "Muscle"
		material_settings_muscle.MassDensity = 1090.4, Unit("kg/m^3")
		material_settings_muscle.ElectricProps.Conductivity = 0.9782042083052804, Unit("S/m")
		material_settings_muscle.ElectricProps.RelativePermittivity = 54.81107626413944
	sim.Add(material_settings_muscle, components_muscle)
	# No materials

	# Sources
	planesrc_settings = sim.AddPlaneWaveSourceSettings(entity__wire_block1)
	options = planesrc_settings.ExcitationType.enum
	planesrc_settings.ExcitationType = options.Harmonic
	planesrc_settings.CenterFrequency = 1., units.GHz

	# Sensors
	# Only using overall field sensor

	# Boundary Conditions
	options = sim.GlobalBoundarySettings.GlobalBoundaryType.enum
	sim.GlobalBoundarySettings.GlobalBoundaryType = options.UpmlCpml


	# Grid
	# AutomaticGridSettings "Automatic"
	# sim.AllSettings の中にあるすべての設定オブジェクトを調べ、その中で、fdtd.AutomaticGridSettings のインスタンスであり、
	# かつ、その Name 属性が "Automatic" であるものだけを抽出し、それらを要素とする新しいリストを作成する。
	automatic_grid_settings = [x for x in sim.AllSettings if isinstance(x, fdtd.AutomaticGridSettings) and x.Name == "Automatic"][0]
	#全てのtissueエンティティとwire_block1をグリッドコンポーネントとして追加
	components_grid = [entity__tissue, entity__wire_block1]
	# 既存の自動グリッド設定にコンポーネントを追加
	sim.Add(automatic_grid_settings, components_grid)
	
	"""" 
	# Grid
	# ManualGridSettings "Manual"
	manual_grid_settings = sim.AddManualGridSettings([entity__wire_block1])
	manual_grid_settings.MaxStep = (9.0,)*3 # model units
	manual_grid_settings.Resolution = (2.0,)*3  # model units
	"""
	   # Voxels
    # AutomaticVoxelerSettings "Automatic Voxeler Settings"
	automatic_voxeler_settings = [x for x in sim.AllSettings if isinstance(x, fdtd.AutomaticVoxelerSettings) and x.Name == "Automatic Voxeler Settings"][0]
    # 全てのtissueエンティティとwire_block1をボクセラーコンポーネントとして追加
	components_voxeler = components_grid # グリッドと同じコンポーネントリストを使用
	sim.Add(automatic_voxeler_settings, components_voxeler)

	""""
	# Voxels
	auto_voxel_settings = sim.AddAutomaticVoxelerSettings(entity__wire_block1)
	"""

	# Solver settings
	options = sim.SolverSettings.Kernel.enum
	sim.SolverSettings.Kernel = options.Software

	return sim

def AnalyzeSimulation(sim):

	# Create extractor for a given simulation output file
	results = sim.Results()

	print(results)

	# overall field sensor
	overall_field_sensor = results[ 'Overall Field' ]

	# Create a slice viewer for the E field
	slice_field_viewer_efield = viewers.SliceFieldViewer()
	slice_field_viewer_efield.Inputs[0].Connect( overall_field_sensor['EM E(x,y,z,f0)'] )
	slice_field_viewer_efield.Data.Mode = slice_field_viewer_efield.Data.Mode.enum.QuantityRealPart
	slice_field_viewer_efield.Data.Component = slice_field_viewer_efield.Data.Component.enum.Component0
	slice_field_viewer_efield.Slice.Plane = slice_field_viewer_efield.Slice.Plane.enum.YZ
	slice_field_viewer_efield.Update(0)
	slice_field_viewer_efield.GotoMaxSlice()
	document.AllAlgorithms.Add( slice_field_viewer_efield )

def RunTutorial():
	import s4l_v1.document
	
	s4l_v1.document.New()

	CreateModel()
	
	sim = CreateSimulation()
	
	s4l_v1.document.AllSimulations.Add(sim)
	sim.UpdateGrid()
	sim.CreateVoxels()
	sim.RunSimulation(wait=True)  # True = wait until simulation has finished
	
	AnalyzeSimulation(sim)

def main(data_path=None, project_dir=None):
	"""
		data_path = path to a folder that contains data for this simulation (e.g. model files)
		project_dir = path to a folder where this project and its results will be saved
	"""
	import sys
	import os
	print("Python ", sys.version)
	print("Running in ", os.getcwd(), "@", os.environ['COMPUTERNAME'])

	"""
	if project_dir is None:
		project_dir = os.path.expanduser(os.path.join('~', 'Documents', 's4l_python_tutorials') )
		
	if not os.path.exists(project_dir):
		os.makedirs(project_dir)

	fname = os.path.splitext(os.path.basename(_CFILE))[0] + '.smash'
	project_path = os.path.join(project_dir, fname)
	"""

	RunTutorial()

if __name__ == '__main__':
	main()