from __future__ import absolute_import
from __future__ import print_function
import sys, os
import numpy as np
import csv # CSVファイル操作のためにcsvモジュールをインポート
import json # JSONデータを扱うためにjsonモジュールをインポート

import s4l_v1.document as document
import s4l_v1.model as model
import s4l_v1.simulation.emfdtd as fdtd
import s4l_v1.analysis as analysis
import s4l_v1.analysis.core as analysis_core
import s4l_v1.analysis.viewers as viewers
import s4l_v1.materials.database as database # 材料データベースのインポートを有効化

import s4l_v1.units as units
from s4l_v1 import ReleaseVersion # ReleaseVersionのインポート
from s4l_v1 import Unit # Unitのインポート

_CFILE = os.path.abspath(sys.argv[0] if __name__ == '__main__' else __file__ )
_CDIR = os.path.dirname(_CFILE)

def CreateModel():
	"""
	既存のモデルからエンティティがロードされることを前提とします。
	この関数は、シミュレーションが実行されるS4Lプロジェクトに
	必要なモデルエンティティ（例: tissue_0, tissue_1, wire_block1 など）が既に存在することを前提とします。
	"""
	pass # 何も作成しない (既存モデルを使用するため)

# --- ここから、単一シミュレーションインスタンス作成のためのヘルパー関数 ---
def _create_single_simulation_instance(sim_name, theta_deg, phi_deg, psi_deg):
	"""
	指定された名前と平面波の到来方向を持つ単一のFDTDシミュレーションインスタンスを作成します。
	この関数は、元のCreateSimulation関数のロジックをベースに、パラメータを受け取るように修正されています。
	"""
	# ReleaseVersionをアクティブに設定
	ReleaseVersion.set_active(ReleaseVersion.version7_2)

	sim = fdtd.Simulation()
	sim.Name = sim_name # シミュレーション名をパラメータから設定

	# モデルから必要なエンティティを取得
	entities = model.AllEntities()

	# 解析条件で指定されたすべてのエンティティをマッピング
	# これらのエンティティがS4Lのモデル内に存在することを前提とします
	# KeyErrorsを防ぐため、存在しないエンティティはスキップするか、デフォルト値を使用するロジックを追加することも可能
	entity_names = [
		"Tissue_0", "Tissue_1", "Tissue_10", "Tissue_11", "Tissue_12", "Tissue_13", "Tissue_14", "Tissue_15",
		"Tissue_17", "Tissue_18", "Tissue_19", "Tissue_2", "Tissue_20", "Tissue_21", "Tissue_22", "Tissue_23",
		"Tissue_24", "Tissue_25", "Tissue_26", "Tissue_28", "Tissue_29", "Tissue_30", "Tissue_31", "Tissue_32",
		"Tissue_33", "Tissue_34", "Tissue_35", "Tissue_37", "Tissue_38", "Tissue_39", "Tissue_4", "Tissue_42",
		"Tissue_43", "Tissue_44", "Tissue_45", "Tissue_46", "Tissue_47", "Tissue_48", "Tissue_49", "Tissue_5",
		"Tissue_50", "Tissue_51", "Tissue_52", "Tissue_53", "Tissue_54", "Tissue_55", "Tissue_56", "Tissue_6",
		"Tissue_7", "Tissue_8", "Tissue_9", "Wire Block 1"
	]
	
	# 実際に存在するエンティティのみを辞書に格納
	mapped_entities = {}
	for name in entity_names:
		if name in entities:
			mapped_entities[name] = entities[name]
		else:
			print(f"WARNING: Entity '{name}' not found in model. Skipping.")

		# 必要なエンティティを直接変数に割り当て (存在しない場合はNoneになる)
	# 番号順に整理
	entity__tissue_0 = mapped_entities.get("Tissue_0")
	entity__tissue_1 = mapped_entities.get("Tissue_1")
	entity__tissue_2 = mapped_entities.get("Tissue_2")
	entity__tissue_4 = mapped_entities.get("Tissue_4")
	entity__tissue_5 = mapped_entities.get("Tissue_5")
	entity__tissue_6 = mapped_entities.get("Tissue_6")
	entity__tissue_7 = mapped_entities.get("Tissue_7")
	entity__tissue_8 = mapped_entities.get("Tissue_8")
	entity__tissue_9 = mapped_entities.get("Tissue_9")
	entity__tissue_10 = mapped_entities.get("Tissue_10")
	entity__tissue_11 = mapped_entities.get("Tissue_11")
	entity__tissue_12 = mapped_entities.get("Tissue_12")
	entity__tissue_13 = mapped_entities.get("Tissue_13")
	entity__tissue_14 = mapped_entities.get("Tissue_14")
	entity__tissue_15 = mapped_entities.get("Tissue_15")
	entity__tissue_17 = mapped_entities.get("Tissue_17")
	entity__tissue_18 = mapped_entities.get("Tissue_18")
	entity__tissue_19 = mapped_entities.get("Tissue_19")
	entity__tissue_20 = mapped_entities.get("Tissue_20")
	entity__tissue_21 = mapped_entities.get("Tissue_21")
	entity__tissue_22 = mapped_entities.get("Tissue_22")
	entity__tissue_23 = mapped_entities.get("Tissue_23")
	entity__tissue_24 = mapped_entities.get("Tissue_24")
	entity__tissue_25 = mapped_entities.get("Tissue_25")
	entity__tissue_26 = mapped_entities.get("Tissue_26")
	entity__tissue_28 = mapped_entities.get("Tissue_28")
	entity__tissue_29 = mapped_entities.get("Tissue_29")
	entity__tissue_30 = mapped_entities.get("Tissue_30")
	entity__tissue_31 = mapped_entities.get("Tissue_31")
	entity__tissue_32 = mapped_entities.get("Tissue_32")
	entity__tissue_33 = mapped_entities.get("Tissue_33")
	entity__tissue_34 = mapped_entities.get("Tissue_34")
	entity__tissue_35 = mapped_entities.get("Tissue_35")
	entity__tissue_37 = mapped_entities.get("Tissue_37")
	entity__tissue_38 = mapped_entities.get("Tissue_38")
	entity__tissue_39 = mapped_entities.get("Tissue_39")
	entity__tissue_42 = mapped_entities.get("Tissue_42")
	entity__tissue_43 = mapped_entities.get("Tissue_43")
	entity__tissue_44 = mapped_entities.get("Tissue_44")
	entity__tissue_45 = mapped_entities.get("Tissue_45")
	entity__tissue_46 = mapped_entities.get("Tissue_46")
	entity__tissue_47 = mapped_entities.get("Tissue_47") # Skin用
	entity__tissue_48 = mapped_entities.get("Tissue_48")
	entity__tissue_49 = mapped_entities.get("Tissue_49")
	entity__tissue_50 = mapped_entities.get("Tissue_50") # Fat用
	entity__tissue_51 = mapped_entities.get("Tissue_51")
	entity__tissue_52 = mapped_entities.get("Tissue_52")
	entity__tissue_53 = mapped_entities.get("Tissue_53")
	entity__tissue_54 = mapped_entities.get("Tissue_54")
	entity__tissue_55 = mapped_entities.get("Tissue_55")
	entity__tissue_56 = mapped_entities.get("Tissue_56")
	entity__wire_block1 = mapped_entities.get("Wire Block 1") # Wire Block 1 は最後に


	# Setup
	setup_settings = sim.SetupSettings
	setup_settings.GlobalAutoTermination = setup_settings.GlobalAutoTermination.enum.GlobalAutoTerminationStrict
	setup_settings.SimulationTime = 30.0, units.Periods # 解析条件に合わせて変更 (元のスクリプトの値を反映)

	# Materials
	# Adding a new MaterialSettings for Fat
	material_settings_fat = fdtd.MaterialSettings()
	components_fat = [entity__tissue_50] if entity__tissue_50 else [] # エンティティが存在する場合のみ追加
	try:
		mat_fat = database["IT'IS 4.1"]["Fat"]
		sim.LinkMaterialWithDatabase(material_settings_fat, mat_fat)
	except Exception as e:
		print(f"Warning: 'Fat' material not found in database or linking failed ({e}). Using fallback values for {sim_name}.")
		material_settings_fat.Name = "Fat"
		material_settings_fat.MassDensity = 911.0, Unit("kg/m^3")
		material_settings_fat.ElectricProps.Conductivity = 0.11638198214029223, Unit("S/m")
		material_settings_fat.ElectricProps.RelativePermittivity = 11.29425354244377
	if components_fat: # コンポーネントが存在する場合のみsim.Add
		sim.Add(material_settings_fat, components_fat)

	# Adding a new MaterialSettings for Skin
	material_settings_skin = fdtd.MaterialSettings()
	components_skin = [entity__tissue_47] if entity__tissue_47 else [] # エンティティが存在する場合のみ追加
	try:
		mat_skin = database["IT'IS 4.1"]["Skin"]
		sim.LinkMaterialWithDatabase(material_settings_skin, mat_skin)
	except Exception as e:
		print(f"Warning: 'Skin' material not found in database or linking failed ({e}). Using fallback values for {sim_name}.")
		material_settings_skin.Name = "Skin"
		material_settings_skin.MassDensity = 1109.0, Unit("kg/m^3")
		material_settings_skin.ElectricProps.Conductivity = 0.8997924135002646, Unit("S/m")
		material_settings_skin.ElectricProps.RelativePermittivity = 40.936135452253346
	if components_skin: # コンポーネントが存在する場合のみsim.Add
		sim.Add(material_settings_skin, components_skin)

	# Adding a new MaterialSettings for Muscle
	material_settings_muscle = fdtd.MaterialSettings()
	components_muscle = [
		entity__tissue_0, entity__tissue_1, entity__tissue_10, entity__tissue_11, entity__tissue_12, entity__tissue_13,
		entity__tissue_14, entity__tissue_15, entity__tissue_17, entity__tissue_18, entity__tissue_19, entity__tissue_2,
		entity__tissue_20, entity__tissue_21, entity__tissue_22, entity__tissue_23, entity__tissue_24, entity__tissue_25,
		entity__tissue_26, entity__tissue_28, entity__tissue_29, entity__tissue_30, entity__tissue_31, entity__tissue_32,
		entity__tissue_33, entity__tissue_34, entity__tissue_35, entity__tissue_37, entity__tissue_38, entity__tissue_39,
		entity__tissue_4, entity__tissue_42, entity__tissue_43, entity__tissue_44, entity__tissue_45, entity__tissue_46,
		entity__tissue_48, entity__tissue_49, entity__tissue_5, entity__tissue_51, entity__tissue_52, entity__tissue_53,
		entity__tissue_54, entity__tissue_55, entity__tissue_56, entity__tissue_6, entity__tissue_7, entity__tissue_8,
		entity__tissue_9
	]
	# Noneのエンティティを除外
	components_muscle = [e for e in components_muscle if e is not None]

	try:
		mat_muscle = database["IT'IS 4.1"]["Muscle"]
		sim.LinkMaterialWithDatabase(material_settings_muscle, mat_muscle)
	except Exception as e:
		print(f"Warning: 'Muscle' material not found in database or linking failed ({e}). Using fallback values for {sim_name}.")
		material_settings_muscle.Name = "Muscle"
		material_settings_muscle.MassDensity = 1090.4, Unit("kg/m^3")
		material_settings_muscle.ElectricProps.Conductivity = 0.9782042083052804, Unit("S/m")
		material_settings_muscle.ElectricProps.RelativePermittivity = 54.81107626413944
	if components_muscle: # コンポーネントが存在する場合のみsim.Add
		sim.Add(material_settings_muscle, components_muscle)

	# Sources
	plane_wave_source_settings = fdtd.PlaneWaveSourceSettings()
	components_source = [entity__wire_block1] if entity__wire_block1 else [] # wire_block1が存在する場合のみ追加
	if not components_source:
		print(f"ERROR: 'Wire Block 1' entity not found for source in {sim_name}. Cannot set up plane wave source.")
		return None # ソース設定不可のためシミュレーション作成を中止

	plane_wave_source_settings.Theta = theta_deg, units.Degrees
	plane_wave_source_settings.Phi = phi_deg, units.Degrees
	plane_wave_source_settings.Psi = psi_deg, units.Degrees # Psi角度をパラメータから設定
	sim.Add(plane_wave_source_settings, components_source)

	# Sensors (元のスクリプトのコメント通り、Overall Field Sensorのみ)
	# Boundary Conditions (元のスクリプトから変更なし)
	options = sim.GlobalBoundarySettings.GlobalBoundaryType.enum
	sim.GlobalBoundarySettings.GlobalBoundaryType = options.UpmlCpml

	# Grid
	# AutomaticGridSettings "Automatic"
	automatic_grid_settings = [x for x in sim.AllSettings if isinstance(x, fdtd.AutomaticGridSettings) and x.Name == "Automatic"][0]
	components_grid_all = [e for e in mapped_entities.values() if e is not None] # 全てのマップされたエンティティをグリッド対象に
	sim.Add(automatic_grid_settings, components_grid_all)

	# Voxels
	# AutomaticVoxelerSettings "Automatic Voxeler Settings"
	automatic_voxeler_settings = [x for x in sim.AllSettings if isinstance(x, fdtd.AutomaticVoxelerSettings) and x.Name == "Automatic Voxeler Settings"][0]
	components_voxeler_all = components_grid_all # グリッドと同じコンポーネントリストを使用
	sim.Add(automatic_voxeler_settings, components_voxeler_all)

	# Solver
	solver_settings = sim.SolverSettings
	solver_settings.Kernel = solver_settings.Kernel.enum.AXware # AXwareソルバーを使用

	# Update the materials with the new frequency parameters
	sim.UpdateAllMaterials() 

	# Update the grid with the new parameters
	sim.UpdateGrid()
	
	return sim

# --- ここから、SAR解析のための関数 ---
def Analyze_WBSAR(sim):
	"""
	指定されたシミュレーションの結果を解析し、
	「Volume Weighted Average」SAR値を抽出し表示します。
	"""
	import json # JSONデータを扱うためにjsonモジュールをインポート

	results = sim.Results()
	print(f"Analysis results for: {sim.Name}")
	print(results)

	em_sensor_extractor = results[ 'Overall Field' ]
	em_sensor_extractor.FrequencySettings.ExtractedFrequency = u"All"
	document.AllAlgorithms.Add( em_sensor_extractor )

	inputs_for_statistics = [em_sensor_extractor.Outputs["SAR(x,y,z,f0)"]]
	statistics_evaluator = analysis_core.StatisticsEvaluator(inputs=inputs_for_statistics)
	statistics_evaluator.Mode = u"Value"
	statistics_evaluator.UpdateAttributes()
	document.AllAlgorithms.Add( statistics_evaluator )
	
	# 統計評価アルゴリズムの計算を強制的に実行
	# Update() が False を返す場合、計算に失敗したことを示す
	if not statistics_evaluator.Update(): # Update()の戻り値で計算成功をチェック
		print(f"DEBUG: StatisticsEvaluator '{statistics_evaluator.Name}' failed to update/compute. Cannot extract SAR statistics.")
		return None # 計算に失敗したため、Noneを返す

	# --- ここからが修正箇所：Volume Weighted Average の値を取得 ---

	# 1. StatisticsEvaluatorの「SAR Statistics」出力（AlgorithmOutputオブジェクト）を取得
	sar_statistics_output_ref = statistics_evaluator.Outputs["SAR Statistics"]

	# 2. AlgorithmOutputオブジェクトの .Data プロパティを使って、JsonDataObjectを取得
	json_data_object = sar_statistics_output_ref.Data

	# デバッグ: 取得したオブジェクトの型を確認
	print(f"DEBUG: Type of json_data_object: {type(json_data_object)}")
	
	# --- ここから JsonDataObject のプロパティをデバッグ出力 ---
	print("\n--- DEBUG: Inspecting JsonDataObject Properties ---")
	
	# DataJson プロパティの確認
	if hasattr(json_data_object, 'DataJson'):
		print(f"DEBUG: json_data_object.DataJson type: {type(json_data_object.DataJson)}")
		print(f"DEBUG: json_data_object.DataJson content (first 300 chars): {str(json_data_object.DataJson)[:300]}...")
	else:
		print("DEBUG: json_data_object has no 'DataJson' attribute.")

	# AttributeJson プロパティの確認
	if hasattr(json_data_object, 'AttributeJson'):
		print(f"DEBUG: json_data_object.AttributeJson type: {type(json_data_object.AttributeJson)}")
		print(f"DEBUG: json_data_object.AttributeJson content (first 300 chars): {str(json_data_object.AttributeJson)[:300]}...")
	else:
		print("DEBUG: json_data_object has no 'AttributeJson' attribute.")

	# keys() メソッドの確認 (辞書のように振る舞うか)
	if hasattr(json_data_object, 'keys') and callable(json_data_object.keys):
		try:
			print(f"DEBUG: json_data_object.keys(): {list(json_data_object.keys())}")
			# もしキーがあれば、最初のキーでアクセスを試みる
			if list(json_data_object.keys()):
				first_key = list(json_data_object.keys())[0]
				print(f"DEBUG: Accessing first key '{first_key}': {json_data_object[first_key]}")
		except Exception as e:
			print(f"DEBUG: Error calling json_data_object.keys() or accessing by key: {e}")
	else:
		print("DEBUG: json_data_object has no 'keys()' method.")

	print("--- DEBUG: End JsonDataObject Inspection ---\n")
	# --- デバッグ出力ここまで ---

	# --- 新しいデータ抽出ロジック: DataJsonからの直接抽出 ---
	volume_weighted_average_value = None

	if hasattr(json_data_object, 'DataJson') and isinstance(json_data_object.DataJson, str):
		try:
			# DataJson文字列をPythonオブジェクト（辞書）にパース
			parsed_data = json.loads(json_data_object.DataJson)
			print("DEBUG: Successfully parsed DataJson string.")

			# デバッグ出力から判明したネストされた構造をたどる
			# {"simple_data_collection":{"data_collection":{"Average":{"data":[VALUE]...
			if "simple_data_collection" in parsed_data and \
			   "data_collection" in parsed_data["simple_data_collection"] and \
			   "Average" in parsed_data["simple_data_collection"]["data_collection"] and \
			   "data" in parsed_data["simple_data_collection"]["data_collection"]["Average"] and \
			   isinstance(parsed_data["simple_data_collection"]["data_collection"]["Average"]["data"], list) and \
			   len(parsed_data["simple_data_collection"]["data_collection"]["Average"]["data"]) > 0:
				
				volume_weighted_average_value = parsed_data["simple_data_collection"]["data_collection"]["Average"]["data"][0]
				print("DEBUG: Extracted Volume Weighted Average value from nested dictionary.")
			else:
				print("DEBUG: Could not find 'Volume Weighted Average' data in expected nested structure.")

		except json.JSONDecodeError as e:
			print(f"ERROR: Failed to decode DataJson string: {e}")
		except Exception as e:
			print(f"ERROR: An unexpected error occurred during data extraction from parsed DataJson: {e}")
	else:
		print("ERROR: JsonDataObject has no 'DataJson' attribute or 'DataJson' is not a string. Cannot extract value.")

	# 最終的な値が取得できたか確認
	if volume_weighted_average_value is not None:
		print(f"Volume Weighted Average for simulation '{sim.Name}': {volume_weighted_average_value} W/kg")
		
		# これで 'volume_weighted_average_value' 変数に目的の値が格納されました。
		# この値を後続の処理やファイルへの書き出しなどに使用できます。
	else:
		print(f"WARNING: 'Volume Weighted Average' not found in SAR Statistics data for {sim.Name} using direct access methods.")

	# --- ここまでが追加コード ---

	# --- DataTableHTMLViewerの初期化と追加 ---
	# 新しいDataTableHTMLViewerを追加
	# ここでは、元のstatistics_evaluatorの出力をそのまま使用します。
	# HTMLビューアはJsonDataObjectを直接表示できる場合が多いです。
	inputs_for_html_viewer = [statistics_evaluator.Outputs["SAR Statistics"]] 
	data_table_html_viewer = viewers.DataTableHTMLViewer(inputs=inputs_for_html_viewer)
	
	# 属性を更新
	data_table_html_viewer.UpdateAttributes()
	# S4Lドキュメントに追加
	document.AllAlgorithms.Add(data_table_html_viewer)
	
	return volume_weighted_average_value # 抽出した値を戻り値として追加

# --- SAR解析結果をCSVファイルに書き込む関数 ---
def write_sar_results_to_csv(results_list, filename="sar_results.csv"):
	"""
	SAR解析結果のリストをCSVファイルに書き込みます。
	ファイルが存在しない場合はヘッダー行を作成し、存在する場合はデータを追記します。

	Args:
		results_list (list): 各要素が辞書形式のSAR結果データを含むリスト。
							 例: [{'SimulationName': '...', 'Direction': '...', 'VWA_SAR': ...}]
		filename (str): 出力するCSVファイルのパスと名前。
	"""
	# ファイルが存在するかどうかを確認し、ヘッダーを書き込む必要があるかを判断
	file_exists = os.path.exists(filename)
	
	# 'a' は追記モード、'w' は上書きモード
	# newline='' はcsvモジュールで推奨される設定
	with open(filename, 'a' if file_exists else 'w', newline='', encoding='utf-8') as csvfile:
		fieldnames = ['SimulationName', 'Direction', 'VWA_SAR'] # CSVの列名
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

		if not file_exists:
			writer.writeheader() # ファイルが新規作成された場合のみヘッダーを書き込む

		for row in results_list:
			writer.writerow(row)
	print(f"\nResults successfully written to '{filename}'.")

# --- 既存のシミュレーションを削除する関数 ---
def delete_all_simulations_in_document():
	"""
	Deletes all simulations currently present in the S4L document.
	This is useful to ensure a clean slate before creating new simulations,
	especially if previous runs left simulations in memory or on the GUI.
	"""
	print("\n--- Deleting existing simulations in document ---")
	# Get a list of all current simulations.
	# It's important to convert to a list because you cannot modify a collection while iterating over it directly.
	sims_to_delete = list(document.AllSimulations) 
	
	if sims_to_delete:
		for sim_to_delete in sims_to_delete:
			print(f"Deleting simulation: {sim_to_delete.Name}")
			document.AllSimulations.Remove(sim_to_delete)
		print("All existing simulations deleted.")
	else:
		print("No existing simulations to delete.")

# --- ここから、単一シミュレーションを実行する関数 ---
def RunSingleSimulation():
	"""
	単一のシミュレーションインスタンスを実行します。
	この関数は新しいドキュメント、モデル、単一のシミュレーションを作成し、
	シミュレーションを実行して全身平均SARを解析します。
	結果はCSVファイルに書き出されます。
	"""
	# document.New() は削除し、既存シミュレーションを削除する関数を呼び出す
	delete_all_simulations_in_document()

	# CreateModel() は削除 (既存モデルを使用するため)
	
	# Create a single simulation instance with default angles and parameters from original CreateSimulation
	# Psi angle is set to 90.0 as per the original CreateSimulation
	sim = _create_single_simulation_instance('Single Run Simulation', 90.0, 180.0, 90.0)
	
	if sim is None: # _create_single_simulation_instanceでエラーがあった場合
		print("ERROR: Failed to create single simulation instance. Aborting RunSingleSimulation.")
		return

	print(f"--- Created simulation: {sim.Name} ---")

	document.AllSimulations.Add(sim) # Add simulation to document
	print(f"--- Added simulation to document: {sim.Name} ---")
	sim.UpdateGrid() # Update grid
	print(f"--- Updated grid for simulation: {sim.Name} ---")
	sim.CreateVoxels() # Create voxels (this call might internally trigger project saving)
	print(f"--- Created voxels for simulation: {sim.Name} ---")
	sim.RunSimulation(wait=True)  # Run simulation (wait for completion)
	print(f"--- Finished running simulation: {sim.Name} ---")

	# Analyze_WBSARから値を取得し、CSVに書き出す
	vwa_sar = Analyze_WBSAR(sim) # Analyze_WBSARから値を取得

	# 単一シミュレーションの結果をリストに格納
	single_sar_result = []
	if vwa_sar is not None:
		single_sar_result.append({
			'SimulationName': sim.Name,
			'Direction': 'Default', # 単一シミュレーションの方向として 'Default' を使用
			'VWA_SAR': vwa_sar
		})
	
	# 単一シミュレーションの結果をCSVファイルに出力
	output_filename = "D:/Users/Kusakabe/Taro_python/single_wbsar_results.csv" # ご自身のパスに変更してください
	if single_sar_result: # 結果がある場合のみ書き出す
		write_sar_results_to_csv(single_sar_result, output_filename)
	else:
		print(f"WARNING: No SAR results to write for single simulation to '{output_filename}'.")

# --- ここから、複数シミュレーションを実行する新しい関数 ---
def RunMultiplePlaneWaveSimulations(model_name):
	"""
	Creates, runs, and analyzes multiple plane wave simulations for a given model.
	The plane wave arrival direction is varied for each simulation.

	Args:
		model_name (str): The name of the anatomical model (e.g., 'Standing Model', 'Seated Model').
	"""
	print(f"--- Starting Multiple Simulations for Model: {model_name} ---")
	
	# Sim4LifeのPython Editorで実行する場合、スクリプト実行前に手動でモデルをロードしておく必要があります。
	print(f"INFO: Assumed model '{model_name}' is already loaded in Sim4Life.")

	# document.New() は削除し、既存シミュレーションを削除する関数を呼び出す
	delete_all_simulations_in_document()

	# CreateModel() は削除 (既存モデルを使用するため)

	# 平面波の到来方向の設定リスト
	# 各タプルは (シミュレーション名サフィックス, Theta角[度], Phi角[度], Psi角[度]) を表します。
	simulation_configs = [
		("Front (Y-)", 90.0, 270.0, 90.0), # 正のY軸から到来
		("Back (Y+)", 90.0, 90.0, 90.0),   # 負のY軸から到来
		("Left (X-)", 90.0, 180.0, 90.0),  # 正のX軸から到来
		("Right (X+)", 90.0, 0.0, 90.0)    # 負のX軸から到来
	]

	all_sar_results = []

	print("\n--- Simulation Creation Phase ---")
	for name_suffix, theta_deg, phi_deg, psi_deg in simulation_configs:
		sim_full_name = f"{model_name} - {name_suffix}"
		print(f"Creating simulation: {sim_full_name} (Theta={theta_deg}, Phi={phi_deg}, Psi={psi_deg})")

		sim_instance = _create_single_simulation_instance(sim_full_name, theta_deg, phi_deg, psi_deg)
		
		if sim_instance is None:
			print(f"ERROR: Failed to create simulation instance '{sim_full_name}'. Skipping.")
			continue

		document.AllSimulations.Add(sim_instance)
		sim_instance.UpdateGrid()
		sim_instance.CreateVoxels() 

	print("\n--- Simulation Execution Phase ---")
	sim_map = {sim.Name: sim for sim in document.AllSimulations}

	for name_suffix, _, _, _ in simulation_configs:
		sim_full_name = f"{model_name} - {name_suffix}"
		sim_to_run = sim_map.get(sim_full_name)

		if sim_to_run:
			print(f"Running simulation: {sim_to_run.Name}...")
			sim_to_run.RunSimulation(wait=True)
			print(f"Finished running simulation: {sim_to_run.Name}")
		else:
			print(f"WARNING: Simulation '{sim_full_name}' not found for execution.")

	print("\n--- Simulation Analysis Phase ---")
	for name_suffix, _, _, _ in simulation_configs:
		sim_full_name = f"{model_name} - {name_suffix}"
		sim_to_analyze = sim_map.get(sim_full_name)

		if sim_to_analyze:
			vwa_sar = Analyze_WBSAR(sim_to_analyze)
			if vwa_sar is not None:
				all_sar_results.append({
					'ModelName': model_name,
					'SimulationName': sim_full_name,
					'Direction': name_suffix.split('(')[0].strip(),
					'VWA_SAR': vwa_sar
				})
		else:
			print(f"WARNING: Simulation '{sim_full_name}' not found for analysis.")

	print("All simulations analyzed.")
	print(f"--- Multiple Simulations Finished for Model: {model_name} ---")

	# CSVファイル名を固定値に設定
	output_filename = "D:/Users/Kusakabe/multiple_simulation_sar_results.csv" # ご自身のパスに変更してください
	write_sar_results_to_csv(all_sar_results, output_filename)


def main(data_path=None, project_dir=None):
	"""
	Entry point of the script.
	"""
	import sys
	import os
	print("Python Version:", sys.version)
	print("Running in:", os.getcwd(), "@", os.environ.get('COMPUTERNAME', 'Unknown'))

	# --- 実行したいワークフローの行だけコメントを外してください ---

	# オプション1: 複数シミュレーションを実行
	RunMultiplePlaneWaveSimulations()

	# オプション2: 単一シミュレーションを実行
	# RunSingleSimulation() 

	# --- プロジェクト保存用の元のコメントアウトブロック ---
	# 必要に応じて保存機能を有効化してください。
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
