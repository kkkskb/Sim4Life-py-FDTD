from __future__ import absolute_import
from __future__ import print_function
import sys, os
import numpy as np

import s4l_v1.document as document
import s4l_v1.model as model
import s4l_v1.simulation.emfdtd as fdtd
import s4l_v1.analysis as analysis
import s4l_v1.analysis.viewers as viewers
#import s4l_v1.materials.database as database # <-- 追加: 材料データベースのインポート

import s4l_v1.units as units
from s4l_v1 import Unit # Unitクラスのインポート (材料データベースのフォールバック値で使用)

_CFILE = os.path.abspath(sys.argv[0] if __name__ == '__main__' else __file__ )
_CDIR = os.path.dirname(_CFILE)

def CreateModel():
	"""
	シミュレーションに必要なモデルエンティティを作成します。
	この関数は一度だけ呼び出され、作成されたエンティティは複数のシミュレーションで共有されます。
	"""
	from s4l_v1.model import Vec3

	# ワイヤーブロック（平面波ソースとして使用）と筋肉ブロックを作成
	wire = model.CreateWireBlock(p0=Vec3(0,0,0), p1=Vec3(100, 100, 100), parametrized=True)
	block1 = model.CreateSolidBlock(p0=Vec3(10,10,10), p1=Vec3(90, 90, 90), parametrized=True)

	# エンティティに名前を設定
	block1.Name = 'Muscle Block'
	wire.Name = 'Plane Wave Source'

# --- ここから、複数のシミュレーション作成のためのヘルパー関数 ---
def _create_single_simulation_instance(sim_name, theta_deg, phi_deg):
	#指定された名前と平面波の到来方向を持つ単一のFDTDシミュレーションインスタンスを作成します。
	# この関数は、元のCreateSimulation関数のロジックをベースに、パラメータを受け取るように修正されています
	
	# モデルから必要なエンティティを取得
	entities = model.AllEntities()
	entity__wire_block1 = entities['Plane Wave Source']
	entity__tissue = entities['Muscle Block']

	sim = fdtd.Simulation()
	sim.Name = sim_name # シミュレーション名をパラメータから設定

	# Setup
	sim.SetupSettings.SimulationTime = 10., units.Periods

	# Materials:
	# Adding a new MaterialSettings for Muscle
	material_settings_muscle = fdtd.MaterialSettings()
	components_muscle = [entity__tissue]
	mat_muscle = None  
	#mat_muscle = database["IT'IS 4.1"]["Muscle"] # 材料databaseにアクセスできる場合はコメントを外す
	if mat_muscle is not None:
		sim.LinkMaterialWithDatabase(material_settings_muscle, mat_muscle)
	else:
		print(f"Warning: 'Muscle' material not found in database for {sim_name}. Using fallback values.")
		material_settings_muscle.Name = "Muscle"
		material_settings_muscle.MassDensity = 1090.4, Unit("kg/m^3")
		material_settings_muscle.ElectricProps.Conductivity = 0.9782042083052804, Unit("S/m")
		material_settings_muscle.ElectricProps.RelativePermittivity = 54.81107626413944
	sim.Add(material_settings_muscle, components_muscle)
	# No materials (このコメントは元のスクリプトのまま残します)

	# Sources
	planesrc_settings = sim.AddPlaneWaveSourceSettings(entity__wire_block1)
	options = planesrc_settings.ExcitationType.enum
	planesrc_settings.ExcitationType = options.Harmonic
	planesrc_settings.CenterFrequency = 1., units.GHz
	planesrc_settings.Theta = theta_deg, units.Degrees # 平面波の到来方向 (Theta)
	planesrc_settings.Phi = phi_deg, units.Degrees     # 平面波の到来方向 (Phi)

	# Sensors
	# Only using overall field sensor (このコメントは元のスクリプトのまま残します)

	# Boundary Conditions
	options = sim.GlobalBoundarySettings.GlobalBoundaryType.enum
	sim.GlobalBoundarySettings.GlobalBoundaryType = options.UpmlCpml

	# Grid
	# AutomaticGridSettings "Automatic"
	# sim.AllSettings の中にあるすべての設定オブジェクトを調べ、その中で、fdtd.AutomaticGridSettings のインスタンスであり、
	# かつ、その Name 属性が "Automatic" であるものだけを抽出し、それらを要素とする新しいリストを作成する。
	automatic_grid_settings = [x for x in sim.AllSettings if isinstance(x, fdtd.AutomaticGridSettings) and x.Name == "Automatic"][0]
	# 全てのtissueエンティティとwire_block1をグリッドコンポーネントとして追加
	components_grid = [entity__tissue, entity__wire_block1]
	# 既存の自動グリッド設定にコンポーネントを追加
	sim.Add(automatic_grid_settings, components_grid)
	
	"""" # 元のスクリプトのコメントアウトされたグリッド設定ブロック
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

	"""" # 元のスクリプトのコメントアウトされたボクセラー設定ブロック
	# Voxels
	auto_voxel_settings = sim.AddAutomaticVoxelerSettings(entity__wire_block1)
	"""

	# Solver settings
	options = sim.SolverSettings.Kernel.enum
	sim.SolverSettings.Kernel = options.Software

	return sim

# --- ここから、元のCreateSimulation関数 (変更なしで残します) ---
def CreateSimulation():
	"""
	元のスクリプトのCreateSimulation関数。
	この関数は、新しい複数シミュレーションのワークフローでは直接使用されませんが、
	元のコード構造を維持するために残しておきます。
	"""
	# retrieve needed entities from model
	entities = model.AllEntities()

	entity__wire_block1 = entities['Plane Wave Source']
	entity__tissue = entities['Muscle Block']  # モデルブロックを取得

	sim = fdtd.Simulation()

	sim.Name = 'Plane Wave Simulation' # 元のデフォルト名

	# Setup
	sim.SetupSettings.SimulationTime = 10., units.Periods

	# Materials:
	# Adding a new MaterialSettings for Muscle
	material_settings_muscle = fdtd.MaterialSettings()
	components_muscle = [entity__tissue]
	#mat_muscle = database["IT'IS 4.1"]["Muscle"]
	mat_muscle = None  # 材料databaseがない場合のフォールバック
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
	# 元のCreateSimulationでは平面波の角度はデフォルト値が使われます

	# Sensors
	# Only using overall field sensor

	# Boundary Conditions
	options = sim.GlobalBoundarySettings.GlobalBoundaryType.enum
	sim.GlobalBoundarySettings.GlobalBoundaryType = options.UpmlCpml


	# Grid
	# AutomaticGridSettings "Automatic"
	automatic_grid_settings = [x for x in sim.AllSettings if isinstance(x, fdtd.AutomaticGridSettings) and x.Name == "Automatic"][0]
	components_grid = [entity__tissue, entity__wire_block1]
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
	"""
	Analyzes the results of the specified simulation and adds viewers.
	"""
	# Get simulation results
	results = sim.Results()

	print(f"Analyzing results for: {sim.Name}")
	print(results)

	# overall field sensor
	overall_field_sensor = results[ 'Overall Field' ]

	# E場のスライスビューアを作成
	slice_field_viewer_efield = viewers.SliceFieldViewer()
	# E場成分（中心周波数f0）をビューアに接続
	slice_field_viewer_efield.Inputs[0].Connect( overall_field_sensor['EM E(x,y,z,f0)'] )
	# データ表示モードと成分を設定（実部・Component0）
	slice_field_viewer_efield.Data.Mode = slice_field_viewer_efield.Data.Mode.enum.QuantityRealPart
	slice_field_viewer_efield.Data.Component = slice_field_viewer_efield.Data.Component.enum.Component0
	# スライス平面をYZ面に設定
	slice_field_viewer_efield.Slice.Plane = slice_field_viewer_efield.Slice.Plane.enum.YZ
	# ビューアを更新し、最大スライス位置へ移動
	slice_field_viewer_efield.Update(0)
	slice_field_viewer_efield.GotoMaxSlice()
	# ビューアをS4Lドキュメントのアルゴリズムとして追加
	document.AllAlgorithms.Add( slice_field_viewer_efield )

# --- ここから、元のRunSingleSimulation関数 ---
def RunSingleSimulation():

	#document.New() # Create a new document

	#CreateModel() # Create model entities

	# Create a single simulation instance with default angles
	sim = _create_single_simulation_instance('Plane Wave Simulation', 0, 0) # Create a single simulation with default angles
	print(f"--- Created simulation: {sim.Name} ---")

	document.AllSimulations.Add(sim) # Add simulation to document
	print(f"--- Added simulation to document: {sim.Name} ---")
	sim.UpdateGrid() # Update grid
	print(f"--- Updated grid for simulation: {sim.Name} ---")
	sim.CreateVoxels() # Create voxels (this call might internally trigger project saving)
	print(f"--- Created voxels for simulation: {sim.Name} ---")
	sim.RunSimulation(wait=True)  # Run simulation (wait for completion)
	print(f"--- Finished running simulation: {sim.Name} ---")

	AnalyzeSimulation(sim) # Analyze simulation results

# --- ここから、複数シミュレーションを実行する新しい関数 ---
def RunMultiplePlaneWaveSimulations():
	"""
	Creates, runs, and analyzes multiple plane wave simulations.
	The plane wave arrival direction is varied for each simulation.
	"""
	print("--- Starting Multiple Simulations ---")
	# Create a new S4L document
	document.New()

	# Create model entities once
	# This ensures the same model is used across all simulations.
	CreateModel()

	# 平面波の到来方向の設定リスト
	# 各タプルは (シミュレーション名サフィックス, Theta角[度], Phi角[度]) を表します。
	# Theta: Z軸からの角度（90度はXY平面上）
	# Phi: XY平面内でX軸からの角度（反時計回り）
	# 伝搬方向は到来方向と逆になります。
	# 例: Phi=0（正のX軸）は、波が負のX軸から到来し、正のX軸方向へ伝搬することを意味します。
	# ここでは前後左右からの到来を想定しています。
	# Front (Y-): 正のY軸から到来し、負のY軸方向へ伝搬
	# Back (Y+): 負のY軸から到来し、正のY軸方向へ伝搬
	# Left (X-): 正のX軸から到来し、負のX軸方向へ伝搬
	# Right (X+): 負のX軸から到来し、正のX軸方向へ伝搬
	simulation_configs = [
		("Front (Y-)", 90.0, 270.0), # Arrives from positive Y-axis (Phi=270°)
		("Back (Y+)", 90.0, 90.0),   # Arrives from negative Y-axis (Phi=90°)
		("Left (X-)", 90.0, 180.0),  # Arrives from positive X-axis (Phi=180°)
		("Right (X+)", 90.0, 0.0)    # Arrives from negative X-axis (Phi=0°)
	]

	# List to store created simulation objects
	created_simulations = []

	print("\n--- Simulation Creation Phase ---")
	for name_suffix, theta_deg, phi_deg in simulation_configs:
		sim_full_name = 'Plane Wave Simulation - ' + name_suffix
		print(f"Creating simulation: {sim_full_name} (Theta={theta_deg}, Phi={phi_deg})")

		# ヘルパー関数を呼び出して単一のシミュレーションインスタンスを作成
		sim_instance = _create_single_simulation_instance(sim_full_name, theta_deg, phi_deg)
		
		# Add simulation to S4L document
		document.AllSimulations.Add(sim_instance)
		
		# Update grid and voxels (this call might internally trigger project saving)
		sim_instance.UpdateGrid()
		sim_instance.CreateVoxels() 

		created_simulations.append(sim_instance) # Add to list for later execution and analysis

	print("\n--- Simulation Execution Phase ---")
	# Run all created simulations sequentially
	for sim_to_run in created_simulations:
		print(f"Running simulation: {sim_to_run.Name}...")
		sim_to_run.RunSimulation(wait=True) # wait=True to wait for simulation completion
		print(f"Finished simulation: {sim_to_run.Name}")

	print("\n--- Simulation Analysis Phase ---")
	# Analyze results for all simulations
	for sim_to_analyze in created_simulations:
		AnalyzeSimulation(sim_to_analyze)
	print("All simulations analyzed.")
	print("--- Multiple Simulations Finished ---")

def main(data_path=None, project_dir=None):
	import sys
	import os
	print("Python Version:", sys.version)
	print("Running in:", os.getcwd(), "@", os.environ.get('COMPUTERNAME', 'Unknown'))

	# --- 単一シミュレーションの実行 ---
	#RunSingleSimulation()

	# --- 複数シミュレーションの実行 ---
	#RunMultiplePlaneWaveSimulations()

	# --- （デバック用）ドキュメントにシミュレーションを追加するためのもの ---
	add_simulation_to_document(None)  # Add a simulation to the document

	# --- 以下のコードは、プロジェクトディレクトリの作成と保存を行うためのもの ---
	"""
	if project_dir is None:
		project_dir = os.path.expanduser(os.path.join('~', 'Documents', 's4l_python_tutorials') )
		
	if not os.path.exists(project_dir):
		os.makedirs(project_dir)

	fname = os.path.splitext(os.path.basename(_CFILE))[0] + '.smash'
	project_path = os.path.join(project_dir, fname)
	"""

if __name__ == '__main__':
	main()
