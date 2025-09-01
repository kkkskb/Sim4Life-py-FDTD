from __future__ import absolute_import
from __future__ import print_function

# Python標準ライブラリ
import sys, os
import numpy as np
import csv
import json

# Sim4Life固有のライブラリ
import s4l_v1.document as document
import s4l_v1.model as model
import s4l_v1.simulation.emfdtd as fdtd
import s4l_v1.analysis as analysis
import s4l_v1.analysis.core as analysis_core
import s4l_v1.analysis.viewers as viewers
import s4l_v1.analysis.em_evaluators as em_evaluators # 追加
import s4l_v1.materials.database as database
import s4l_v1.units as units
from s4l_v1 import ReleaseVersion
from s4l_v1 import Unit

_CFILE = os.path.abspath(sys.argv[0] if __name__ == '__main__' else __file__ )
_CDIR = os.path.dirname(_CFILE)

# --- ここから、モデルエンティティを作成する関数 ---
def _create_model():
	"""
	Sim4Lifeドキュメントに'Wire Block 1'という名前のエンティティが存在しない場合に、
	新しいWire Blockを作成します。
	"""
	from s4l_v1.model import Vec3
	
	# 既存のモデルエンティティリストを取得
	entities = model.AllEntities()
	
	# 'Wire Block 1'が既に存在するかチェック
	if 'Wire Block 1' in entities:
		print("INFO: 'Wire Block 1' already exists in the document. Skipping creation.")
		pass # 既存の場合は何もしない
	else:
		# 存在しない場合のみ新しいワイヤーブロックを作成
		print("INFO: 'Wire Block 1' not found. Creating a new one.")
		wire = model.CreateWireBlock(p0=Vec3(-100,-100,-100), p1=Vec3(1800, 1800, 1800), parametrized=True)
		wire.Name = 'Wire Block 1'
		
# --- ここから、単一シミュレーションインスタンス作成のためのヘルパー関数 ---
def _create_single_simulation_instance(sim_name, theta_deg, phi_deg, psi_deg, use_simple_model=False):
	"""
	指定された名前と平面波の到来方向を持つ単一のFDTDシミュレーションインスタンスを作成します。
	use_simple_modelフラグに基づいて、使用するエンティティと材料を切り替えます。
	"""
	# ReleaseVersionをアクティブに設定
	ReleaseVersion.set_active(ReleaseVersion.version7_2)

	sim = fdtd.Simulation()
	sim.Name = sim_name # シミュレーション名をパラメータから設定

	# モデルから必要なエンティティを取得
	entities = model.AllEntities()

	# エンティティとコンポーネントリストの初期化
	components_fat = []
	components_skin = []
	components_muscle = []
	components_source = []
	components_grid_all = []
	components_voxeler_all = []

	if use_simple_model:
		# デバッグ用シンプルモデルのエンティティを使用
		entity__wire_block1 = entities.get("Debug Source Wire")
		entity__debug_box = entities.get("Debug Box") 
		
		if not entity__wire_block1 or not entity__debug_box:
			print(f"ERROR: Debug model entities 'Debug Box' or 'Debug Source Wire' not found for {sim_name}. Ensure _create_model(use_simple_model=True) was called.")
			return None

		components_muscle = [entity__debug_box] # デバッグボックスを筋肉として扱う
		components_source = [entity__wire_block1]
		components_grid_all = [entity__debug_box, entity__wire_block1]
		components_voxeler_all = [entity__debug_box, entity__wire_block1]

		# シンプルなデバッグ用材料を設定
		material_settings_debug = fdtd.MaterialSettings()
		material_settings_debug.Name = "DebugMaterial"
		material_settings_debug.MassDensity = 1000.0, Unit("kg/m^3")
		material_settings_debug.ElectricProps.Conductivity = 0.5, Unit("S/m")
		material_settings_debug.ElectricProps.RelativePermittivity = 50.0
		sim.Add(material_settings_debug, components_muscle) # デバッグ材料をデバッグボックスに割り当て

	else:
		# 複雑な人体モデルのエンティティを使用 (元のスクリプトのロジック)
		entity_names = [
			"Tissue_0", "Tissue_1", "Tissue_10", "Tissue_11", "Tissue_12", "Tissue_13", "Tissue_14", "Tissue_15",
			"Tissue_17", "Tissue_18", "Tissue_19", "Tissue_2", "Tissue_20", "Tissue_21", "Tissue_22", "Tissue_23",
			"Tissue_24", "Tissue_25", "Tissue_26", "Tissue_28", "Tissue_29", "Tissue_30", "Tissue_31", "Tissue_32",
			"Tissue_33", "Tissue_34", "Tissue_35", "Tissue_37", "Tissue_38", "Tissue_39", "Tissue_4", "Tissue_42",
			"Tissue_43", "Tissue_44", "Tissue_45", "Tissue_46", "Tissue_47", "Tissue_48", "Tissue_49", "Tissue_5",
			"Tissue_50", "Tissue_51", "Tissue_52", "Tissue_53", "Tissue_54", "Tissue_55", "Tissue_56", "Tissue_6",
			"Tissue_7", "Tissue_8", "Tissue_9", "Wire Block 1"
		]
		
		mapped_entities = {}
		for name in entity_names:
			if name in entities:
				mapped_entities[name] = entities[name]
			else:
				print(f"WARNING: Entity '{name}' not found in model. Skipping.")

		# 必要なエンティティを直接変数に割り当て (存在しない場合はNoneになる)
		entity__wire_block1 = mapped_entities.get("Wire Block 1")
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

		# Materials (元の複雑な材料割り当てロジック)
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
		components_muscle_complex = [ # 既存の複雑なモデル用筋肉コンポーネント
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
		components_muscle = [e for e in components_muscle_complex if e is not None]

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

		# ソース、グリッド、ボクセルの対象エンティティリストを構築
		components_source = [entity__wire_block1] if entity__wire_block1 else []
		components_grid_all = [e for e in mapped_entities.values() if e is not None]
		components_voxeler_all = components_grid_all


	# Setup
	setup_settings = sim.SetupSettings
	setup_settings.GlobalAutoTermination = setup_settings.GlobalAutoTermination.enum.GlobalAutoTerminationStrict
	setup_settings.SimulationTime = 30.0, units.Periods 

	# Sources
	plane_wave_source_settings = fdtd.PlaneWaveSourceSettings()
	if not components_source: # ソースエンティティがない場合はエラー
		print(f"ERROR: No source components available for {sim_name}. Cannot set up plane wave source.")
		return None 
	plane_wave_source_settings.Theta = theta_deg, units.Degrees
	plane_wave_source_settings.Phi = phi_deg, units.Degrees
	plane_wave_source_settings.Psi = psi_deg, units.Degrees
	sim.Add(plane_wave_source_settings, components_source)

	# Sensors (Overall Field Sensorのみ)
	# Boundary Conditions
	options = sim.GlobalBoundarySettings.GlobalBoundaryType.enum
	sim.GlobalBoundarySettings.GlobalBoundaryType = options.UpmlCpml

	# Grid
	automatic_grid_settings = [x for x in sim.AllSettings if isinstance(x, fdtd.AutomaticGridSettings) and x.Name == "Automatic"][0]
	sim.Add(automatic_grid_settings, components_grid_all)

	# Voxels
	automatic_voxeler_settings = [x for x in sim.AllSettings if isinstance(x, fdtd.AutomaticVoxelerSettings) and x.Name == "Automatic Voxeler Settings"][0]
	sim.Add(automatic_voxeler_settings, components_voxeler_all)

	# Solver: AXwareを試し、失敗した場合はSoftwareにフォールバックする
	solver_settings = sim.SolverSettings
	options = solver_settings.Kernel.enum
	try:
		# まずGPUベースのAXwareソルバーを試す
		solver_settings.Kernel = options.AXware
		print("INFO: Attempting to use AXware GPU solver.")
	except Exception as e:
		# ライセンスエラーなどが発生した場合にSoftwareにフォールバック
		print(f"WARNING: Failed to set AXware solver due to: {e}. Falling back to Software (CPU) solver.")
		solver_settings.Kernel = options.Software
	
	sim.UpdateAllMaterials() 
	sim.UpdateGrid()
	
	return sim

# --- ここから、SAR解析のための関数 ---
def _analyze_wbsar(sim):
    """
    指定されたシミュレーションの結果を解析し、
    「All Regions」の「Mass-Averaged SAR」値を抽出し表示します。
    """
    print(f"Analysis results for: {sim.Name}")

    results = sim.Results()
    
    if 'Overall Field' not in results:
        print(f"ERROR: Overall Field sensor not found for {sim.Name}.")
        return None
        
    em_sensor_extractor = results['Overall Field']
    em_sensor_extractor.FrequencySettings.ExtractedFrequency = u"All"
    document.AllAlgorithms.Add(em_sensor_extractor)

    if "EM E(x,y,z,f0)" not in em_sensor_extractor.Outputs:
        print(f"ERROR: 'EM E(x,y,z,f0)' output port not found in the Overall Field sensor.")
        print("This indicates the FDTD simulation did not produce the necessary electric field data.")
        return None

    em_field_output = em_sensor_extractor.Outputs["EM E(x,y,z,f0)"]
    if em_field_output.Data is None:
        print(f"ERROR: 'EM E(x,y,z,f0)' output data is None. The simulation results might be missing or incomplete.")
        return None

    inputs_for_sar_statistics = [em_field_output]
    sar_statistics_evaluator_name = f"SAR Statistics for {sim.Name}"
    if sar_statistics_evaluator_name in document.AllAlgorithms:
        sar_statistics_evaluator = document.AllAlgorithms[sar_statistics_evaluator_name]
        print(f"INFO: Found existing SarStatisticsEvaluator '{sar_statistics_evaluator_name}'.")
    else:
        sar_statistics_evaluator = em_evaluators.SarStatisticsEvaluator(inputs=inputs_for_sar_statistics)
        sar_statistics_evaluator.Name = sar_statistics_evaluator_name
        sar_statistics_evaluator.PeakSpatialAverageSAR = True
        sar_statistics_evaluator.UpdateAttributes()
        document.AllAlgorithms.Add(sar_statistics_evaluator)
        print(f"INFO: Created new SarStatisticsEvaluator '{sar_statistics_evaluator_name}'.")

    if not sar_statistics_evaluator.Update():
        print(f"ERROR: SarStatisticsEvaluator '{sar_statistics_evaluator.Name}' failed to update/compute.")
        return None
    else:
        print(f"INFO: SarStatisticsEvaluator '{sar_statistics_evaluator.Name}' successfully computed.")
        if "SAR Statistics" in sar_statistics_evaluator.Outputs:
            inputs_for_html_viewer = [sar_statistics_evaluator.Outputs["SAR Statistics"]]
            data_table_html_viewer = viewers.DataTableHTMLViewer(inputs=inputs_for_html_viewer)
            data_table_html_viewer.UpdateAttributes()
            document.AllAlgorithms.Add(data_table_html_viewer)
            print(f"INFO: DataTableHTMLViewer '{data_table_html_viewer.Name}' has been added to the document.")

    mass_averaged_sar_value = None

    try:
        if "SAR Statistics" not in sar_statistics_evaluator.Outputs:
            print("ERROR: 'SAR Statistics' output port not found.")
            return None

        sar_statistics_output_ref = sar_statistics_evaluator.Outputs["SAR Statistics"]
        table_data_obj = sar_statistics_output_ref.Data

        if table_data_obj is None:
            print("ERROR: SarStatisticsEvaluator did not produce valid table data.")
            return None
        
        # `ToList()` メソッドでテーブルをリストに変換
        if hasattr(table_data_obj, 'ToList') and callable(table_data_obj.ToList):
            table_list = table_data_obj.ToList()
            
            if not isinstance(table_list, list) or len(table_list) < 1:
                print("WARNING: ToList() did not return a valid list with at least one data row.")
                return None
            
            # `Mass-Averaged SAR` の列インデックスを目視で確認した `2` に固定
            col_index = 2
            
            # `All Regions` 行はリストの最後の要素
            row_index = -1
            
            if col_index < len(table_list[0]) and len(table_list) > 0:
                last_row_values = table_list[row_index]
                if isinstance(last_row_values, list) and col_index < len(last_row_values):
                    mass_averaged_sar_value = last_row_values[col_index]
                else:
                    print("WARNING: Last row is not a list or column index is out of range.")
            else:
                print("WARNING: Could not extract value. Table is empty or column index is invalid.")
        else:
            print("ERROR: TableData object has no 'ToList' method.")
            return None

    except Exception as e:
        print(f"ERROR: An unexpected error occurred during data extraction: {e}")
        return None
    
    if mass_averaged_sar_value is not None:
        print(f"Mass-Averaged SAR (All Regions) for '{sim.Name}': {mass_averaged_sar_value} W/kg")
    else:
        print(f"WARNING: 'Mass-Averaged SAR' value not found for {sim.Name}.")

    return mass_averaged_sar_value

# --- SAR解析デバッグ用の関数 ---
def debug_analyze_sar(outptut_filename):
    sim_names = [sim.Name for sim in document.AllSimulations]

    if not sim_names:
        print(f"ERROR: No simulations found in the current document. Please load a project file with completed simulations.")
        return False
    
    sim_name = sim_names[0]
    sim_to_analyze = document.AllSimulations[sim_name]
    
    print(f"\n--- Starting SAR analysis for: {sim_to_analyze.Name} ---")
    extracted_sar = _analyze_wbsar(sim_to_analyze)

    if extracted_sar is not None:
        print(f"\nSuccessfully extracted Mass-Averaged SAR: {extracted_sar} W/kg")
        
        # CSVファイルに結果を書き込む
        model_name = _get_simulation_info_from_document()
        doc_path = os.path.dirname(document.FileName) if document.FileName else _CDIR
        output_filename = outptut_filename
        
        sar_results = [{
            'ModelName': model_name,
            'SimulationName': sim_name,
            'Direction': sim_name.split(' - ')[-1] if ' - ' in sim_name else 'N/A',
            'MassAveragedSAR': extracted_sar
        }]
        
        _write_mass_averaged_sar_to_csv(sar_results, output_filename)
        
        return True
    else:
        print("\nFailed to extract SAR value.")
        return False

# --- SAR解析結果をCSVファイルに書き込む関数 ---
def _write_mass_averaged_sar_to_csv(results_list, filename):
    """
    SAR解析結果のリストをCSVファイルに書き込みます。
    ファイルが存在しない場合はヘッダー行を作成し、存在する場合はデータを追記します。
    """
    file_exists = os.path.exists(filename)
    
    with open(filename, 'a' if file_exists else 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['ModelName', 'SimulationName', 'Direction', 'MassAveragedSAR'] 
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        for row in results_list:
            writer.writerow(row)
    print(f"\nResults successfully written to '{filename}'.")

# --- モデル名とCSV出力ファイルパスを取得する関数 ---
def _get_simulation_info_from_document():
	"""
	Sim4Lifeドキュメントからモデル名を取得します。
	ドキュメントが未保存の場合は、デフォルト名を返します。

	Returns:

	
		str: モデル名
	"""
	# 現在開いているドキュメントのファイル名を取得します。
	smash_file_path = document.FileName
	
	if not smash_file_path:
		# ドキュメントが保存されていない場合、デフォルトのモデル名を使用
		model_name = "Standing Model"
		print(f"INFO: Document not saved. Using default model name: '{model_name}'.")
		return model_name
	else:
		# 保存済みのドキュメントがある場合、そのファイル名からモデル名を生成
		base_name = os.path.basename(smash_file_path)
		model_name = os.path.splitext(base_name)[0]
		print(f"INFO: Document saved at '{smash_file_path}'. Using model name: '{model_name}'.")
		return model_name

# --- 既存のシミュレーションを削除する関数 ---
def _delete_all_simulations_in_document():
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

# --- ここから、複数シミュレーションを実行する新しい関数 ---
def run_multiple_plane_wave_simulations(output_filename):
	"""
	Creates, runs, and analyzes multiple plane wave simulations for a given model.
	The plane wave arrival direction is varied for each simulation (12 directions in XY plane, vertical and horizontal polarization).

	Args:
		output_filename (str): The name of the output CSV file.
		use_simple_model (bool): If True, creates and uses simple debug model entities.
								 If False, assumes complex anatomical model is loaded.
	"""

	# モデルを作成
	_create_model()

	model_name = _get_simulation_info_from_document() # モデル名を取得

	print(f"--- Starting Multiple Simulations for Model: {model_name} ---")
	print(f"INFO: Assumed model '{model_name}' is already loaded in Sim4Life.")

	# 既存のシミュレーションを削除
	_delete_all_simulations_in_document()

	# 平面波の到来方向と偏波の設定リスト (XY平面上を30度おきの計12方向 x 2偏波)
	# 各タプルは (シミュレーション名サフィックス, Theta角[度], Phi角[度], Psi角[度]) を表します。
	# Theta: Z軸からの角度（990度はXY平面上）
	# Phi: XY平面内でX軸からの角度（反時計回り）
	# Psi: Eフィールドの偏波角度 (90.0: 垂直偏波, 0.0: 水平偏波)
	simulation_configs = []
	polarizations = {"VPol": 90.0, "HPol": 0.0} # 偏波タイプと対応するPsi角度の辞書

	for pol_name, psi_angle in polarizations.items():
		for phi_angle in range(0, 360, 30): # 0, 30, ..., 330
			name_suffix = f"Phi_{phi_angle:03d}_{pol_name}" # 例: "Phi_000_VPol", "Phi_030_HPol"
			simulation_configs.append((name_suffix, 90.0, float(phi_angle), psi_angle))

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
			sim_to_run.RunSimulation(wait=False) # 解析完了を待たずにジョブの提出をする
			print(f"Finished running simulation: {sim_to_run.Name}")
		else:
			print(f"WARNING: Simulation '{sim_full_name}' not found for execution.")

	print("\n--- Simulation Analysis Phase ---")
	for name_suffix, _, _, _ in simulation_configs:
		sim_full_name = f"{model_name} - {name_suffix}"
		sim_to_analyze = sim_map.get(sim_full_name)

		if sim_to_analyze:
			vwa_sar = _analyze_wbsar(sim_to_analyze)
			if vwa_sar is not None:
				all_sar_results.append({
					'ModelName': model_name,
					'SimulationName': sim_full_name,
					'Direction': name_suffix, # 方向名にPhi角度と偏波情報が含まれる
					'VWA_SAR': vwa_sar
				})
		else:
			print(f"WARNING: Simulation '{sim_full_name}' not found for analysis.")
			

	print("All simulations analyzed.")
	print(f"--- Multiple Simulations Finished for Model: {model_name} ---")

	# 結果をCSVファイルに書き出す
	_write_sar_results_to_csv(all_sar_results, output_filename)

# --- 単一シミュレーションを実行する新しい関数 ---
def run_single_plane_wave_simulation(theta_deg, phi_deg, psi_deg, output_filename):
	"""
	指定された単一の角度と偏波で平面波シミュレーションを実行、解析します。

	Args:
		theta_deg (float): Z軸からの到来角度 (度)。
		phi_deg (float): XY平面内での到来角度 (度)。
		psi_deg (float): Eフィールドの偏波角度 (度)。
		output_filename (str): SAR結果を書き込むCSVファイルのパス。
	"""
	_create_model()
	model_name = _get_simulation_info_from_document()

	print(f"--- Starting Single Simulation for Model: {model_name} ---")
	print(f"INFO: Assumed model '{model_name}' is already loaded in Sim4Life.")

	# 既存のシミュレーションを全て削除して、クリーンな状態にする
	_delete_all_simulations_in_document()

	# シミュレーション名と設定を構築
	name_suffix = f"Theta_{theta_deg}_Phi_{phi_deg}_Psi_{psi_deg}"
	sim_full_name = f"{model_name} - {name_suffix}"

	print(f"Creating and running simulation: {sim_full_name}...")

	# シミュレーションインスタンスを作成
	sim_instance = _create_single_simulation_instance(sim_full_name, theta_deg, phi_deg, psi_deg)

	if sim_instance is None:
		print(f"ERROR: Failed to create simulation instance '{sim_full_name}'. Exiting.")
		return

	# S4Lドキュメントにシミュレーションを追加
	document.AllSimulations.Add(sim_instance)

	# グリッドとボクセルを更新
	sim_instance.UpdateGrid()
	sim_instance.CreateVoxels()

	# シミュレーションを実行
	sim_instance.RunSimulation(wait=True)
	print(f"Finished running simulation: {sim_instance.Name}")

	# 解析を実行
	vwa_sar = _analyze_wbsar(sim_instance)
	
	# 結果をCSVに書き出す
	if vwa_sar is not None:
		sar_results = [{
			'ModelName': model_name,
			'SimulationName': sim_full_name,
			'Direction': name_suffix,
			'VWA_SAR': vwa_sar
		}]
		_write_sar_results_to_csv(sar_results, output_filename)
	else:
		print(f"WARNING: No SAR result to write for simulation: {sim_full_name}")

	print("--- Single Simulation Finished ---")

def main(data_path=None, project_dir=None):
	import sys
	import os
	print("Python Version:", sys.version)

	# 単一シミュレーション用の専用ファイル名を推奨
	single_run_output_filename = "E:\Kusaskabe\wbsar_single_result.csv"
	multi_run_output_filename = "E:\Kusaskabe\wbsar_results.csv"

	# --- 以下の行を有効/無効にして、実行したいモードを切り替えてください ---

	# 既存のシミュレーションに対してSAR解析を実行するデバッグ用関数
	debug_analyze_sar(single_run_output_filename) 

	# 単一のシミュレーションを実行する (デフォルト)
	# 正面からの到来 (Phi=0度), 垂直偏波 (Psi=90度)
	#run_single_plane_wave_simulation(theta_deg=90.0, phi_deg=0.0, psi_deg=90.0, output_filename=single_run_output_filename)

	# 複数のシミュレーションを実行する
	# run_multiple_plane_wave_simulations(multi_run_output_filename)

if __name__ == '__main__':
	main()
