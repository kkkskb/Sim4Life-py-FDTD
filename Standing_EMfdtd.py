from __future__ import absolute_import
from __future__ import print_function
import sys, os
import numpy as np

import s4l_v1.document as document
import s4l_v1.model as model
import s4l_v1.simulation.emfdtd as fdtd
import s4l_v1.analysis as analysis
import s4l_v1.analysis.core as analysis_core
import s4l_v1.analysis.viewers as viewers
import s4l_v1.materials.database as database # <-- 追加: 材料データベースのインポート

import s4l_v1.units as units
from s4l_v1 import ReleaseVersion # <-- 追加: ReleaseVersionのインポート
from s4l_v1 import Unit # <-- 追加: Unitのインポート

_CFILE = os.path.abspath(sys.argv[0] if __name__ == '__main__' else __file__ )
_CDIR = os.path.dirname(_CFILE)


def CreateModel():
    # 既存のモデルからエンティティがロードされることを前提とします。
    # この関数は、シミュレーションが実行されるS4Lプロジェクトに
    # 必要なモデルエンティティ（例: tissue_0, tissue_1, wire_block1 など）が既に存在することを前提とします。
    pass # 何も作成しない

def CreateSimulation():

    # ReleaseVersionをアクティブに設定
    ReleaseVersion.set_active(ReleaseVersion.version7_2)

    # Creating the simulation
    sim = fdtd.Simulation() # 'sim'という変数名を使用
    sim.Name = "EM_Py_Test" # 解析条件からシミュレーション名を変更

    # retrieve needed entities from model
    entities = model.AllEntities()

    # 解析条件で指定されたすべてのエンティティをマッピング
    # これらのエンティティがS4Lのモデル内に存在することを前提とします
    entity__tissue_7 = entities["Tissue_7"]
    entity__tissue_1 = entities["Tissue_1"]
    entity__tissue_45 = entities["Tissue_45"]
    entity__tissue_12 = entities["Tissue_12"]
    entity__tissue_23 = entities["Tissue_23"]
    entity__tissue_25 = entities["Tissue_25"]
    entity__tissue_20 = entities["Tissue_20"]
    entity__tissue_26 = entities["Tissue_26"]
    entity__tissue_8 = entities["Tissue_8"]
    entity__tissue_49 = entities["Tissue_49"]
    entity__tissue_24 = entities["Tissue_24"]
    entity__tissue_18 = entities["Tissue_18"]
    entity__tissue_0 = entities["Tissue_0"]
    entity__tissue_35 = entities["Tissue_35"]
    entity__tissue_19 = entities["Tissue_19"]
    entity__tissue_39 = entities["Tissue_39"]
    entity__tissue_50 = entities["Tissue_50"]
    entity__tissue_52 = entities["Tissue_52"]
    entity__tissue_44 = entities["Tissue_44"]
    entity__tissue_54 = entities["Tissue_54"]
    entity__tissue_13 = entities["Tissue_13"]
    entity__tissue_22 = entities["Tissue_22"]
    entity__tissue_4 = entities["Tissue_4"]
    entity__tissue_30 = entities["Tissue_30"]
    entity__tissue_46 = entities["Tissue_46"]
    entity__tissue_29 = entities["Tissue_29"]
    entity__wire_block1 = entities["Wire Block 1"] # <-- Plane Wave Sourceの代わりに使用
    entity__tissue_31 = entities["Tissue_31"]
    entity__tissue_48 = entities["Tissue_48"]
    entity__tissue_9 = entities["Tissue_9"]
    entity__tissue_10 = entities["Tissue_10"]
    entity__tissue_15 = entities["Tissue_15"]
    entity__tissue_14 = entities["Tissue_14"]
    entity__tissue_33 = entities["Tissue_33"]
    entity__tissue_17 = entities["Tissue_17"]
    entity__tissue_32 = entities["Tissue_32"]
    entity__tissue_43 = entities["Tissue_43"]
    entity__tissue_28 = entities["Tissue_28"]
    entity__tissue_51 = entities["Tissue_51"]
    entity__tissue_53 = entities["Tissue_53"]
    entity__tissue_34 = entities["Tissue_34"]
    entity__tissue_6 = entities["Tissue_6"]
    entity__tissue_42 = entities["Tissue_42"]
    entity__tissue_37 = entities["Tissue_37"]
    entity__tissue_38 = entities["Tissue_38"]
    entity__tissue_5 = entities["Tissue_5"]
    entity__tissue_56 = entities["Tissue_56"]
    entity__tissue_11 = entities["Tissue_11"]
    entity__tissue_2 = entities["Tissue_2"]
    entity__tissue_55 = entities["Tissue_55"]
    entity__tissue_47 = entities["Tissue_47"]
    entity__tissue_21 = entities["Tissue_21"]

    # Setup
    setup_settings = sim.SetupSettings # 'sim' を使用
    setup_settings.GlobalAutoTermination = setup_settings.GlobalAutoTermination.enum.GlobalAutoTerminationStrict
    setup_settings.SimulationTime = 30.0, units.Periods # 解析条件に合わせて変更

    # Materials
    # Adding a new MaterialSettings for Fat
    material_settings_fat = fdtd.MaterialSettings()
    components_fat = [entity__tissue_50]
    mat_fat = database["IT'IS 4.1"]["Fat"]
    if mat_fat is not None:
        sim.LinkMaterialWithDatabase(material_settings_fat, mat_fat)
    else:
        print("Warning: 'Fat' material not found in database. Using fallback values.")
        material_settings_fat.Name = "Fat"
        material_settings_fat.MassDensity = 911.0, Unit("kg/m^3")
        material_settings_fat.ElectricProps.Conductivity = 0.11638198214029223, Unit("S/m")
        material_settings_fat.ElectricProps.RelativePermittivity = 11.29425354244377
    sim.Add(material_settings_fat, components_fat)

    # Adding a new MaterialSettings for Skin
    material_settings_skin = fdtd.MaterialSettings()
    components_skin = [entity__tissue_47]
    mat_skin = database["IT'IS 4.1"]["Skin"]
    if mat_skin is not None:
        sim.LinkMaterialWithDatabase(material_settings_skin, mat_skin)
    else:
        print("Warning: 'Skin' material not found in database. Using fallback values.")
        material_settings_skin.Name = "Skin"
        material_settings_skin.MassDensity = 1109.0, Unit("kg/m^3")
        material_settings_skin.ElectricProps.Conductivity = 0.8997924135002646, Unit("S/m")
        material_settings_skin.ElectricProps.RelativePermittivity = 40.936135452253346
    sim.Add(material_settings_skin, components_skin)

    # Adding a new MaterialSettings for Muscle
    material_settings_muscle = fdtd.MaterialSettings()
    components_muscle = [entity__tissue_0, entity__tissue_1, entity__tissue_10, entity__tissue_11, entity__tissue_12, entity__tissue_13, entity__tissue_14, entity__tissue_15, entity__tissue_17, entity__tissue_18, entity__tissue_19, entity__tissue_2, entity__tissue_20, entity__tissue_21, entity__tissue_22, entity__tissue_23, entity__tissue_24, entity__tissue_25, entity__tissue_26, entity__tissue_28, entity__tissue_29, entity__tissue_30, entity__tissue_31, entity__tissue_32, entity__tissue_33, entity__tissue_34, entity__tissue_35, entity__tissue_37, entity__tissue_38, entity__tissue_39, entity__tissue_4, entity__tissue_42, entity__tissue_43, entity__tissue_44, entity__tissue_45, entity__tissue_46, entity__tissue_48, entity__tissue_49, entity__tissue_5, entity__tissue_51, entity__tissue_52, entity__tissue_53, entity__tissue_54, entity__tissue_55, entity__tissue_56, entity__tissue_6, entity__tissue_7, entity__tissue_8, entity__tissue_9]
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

    # Sources
    plane_wave_source_settings = fdtd.PlaneWaveSourceSettings()
    components_source = [entity__wire_block1] # wire_block1をソースのコンポーネントとして使用
    plane_wave_source_settings.Theta = 90.0, units.Degrees
    plane_wave_source_settings.Phi = 180.0, units.Degrees
    plane_wave_source_settings.Psi = 90.0, units.Degrees
    sim.Add(plane_wave_source_settings, components_source)

    # Sensors
    # Overall Field Sensor,解析条件にもOverall Field Sensorしか言及なし

    # Boundary Conditions (元のスクリプトから変更なし)
    options = sim.GlobalBoundarySettings.GlobalBoundaryType.enum
    sim.GlobalBoundarySettings.GlobalBoundaryType = options.UpmlCpml

    # Grid
    # AutomaticGridSettings "Automatic"
    automatic_grid_settings = [x for x in sim.AllSettings if isinstance(x, fdtd.AutomaticGridSettings) and x.Name == "Automatic"][0]
    # 全てのtissueエンティティとwire_block1をグリッドコンポーネントとして追加
    components_grid = [entity__tissue_0, entity__tissue_1, entity__tissue_10, entity__tissue_11, entity__tissue_12, entity__tissue_13, entity__tissue_14, entity__tissue_15, entity__tissue_17, entity__tissue_18, entity__tissue_19, entity__tissue_2, entity__tissue_20, entity__tissue_21, entity__tissue_22, entity__tissue_23, entity__tissue_24, entity__tissue_25, entity__tissue_26, entity__tissue_28, entity__tissue_29, entity__tissue_30, entity__tissue_31, entity__tissue_32, entity__tissue_33, entity__tissue_34, entity__tissue_35, entity__tissue_37, entity__tissue_38, entity__tissue_39, entity__tissue_4, entity__tissue_42, entity__tissue_43, entity__tissue_44, entity__tissue_45, entity__tissue_46, entity__tissue_47, entity__tissue_48, entity__tissue_49, entity__tissue_5, entity__tissue_50, entity__tissue_51, entity__tissue_52, entity__tissue_53, entity__tissue_54, entity__tissue_55, entity__tissue_56, entity__tissue_6, entity__tissue_7, entity__tissue_8, entity__tissue_9, entity__wire_block1]
    sim.Add(automatic_grid_settings, components_grid)
    # Note: 元のスクリプトにあった manual_grid_settings の行はAutomaticGridSettingsと重複するため削除

    # Voxels
    # AutomaticVoxelerSettings "Automatic Voxeler Settings"
    automatic_voxeler_settings = [x for x in sim.AllSettings if isinstance(x, fdtd.AutomaticVoxelerSettings) and x.Name == "Automatic Voxeler Settings"][0]
    # 全てのtissueエンティティとwire_block1をボクセラーコンポーネントとして追加
    components_voxeler = components_grid # グリッドと同じコンポーネントリストを使用
    sim.Add(automatic_voxeler_settings, components_voxeler)
    # Note: 元のスクリプトにあった auto_voxel_settings の行はAutomaticVoxelerSettingsと重複するため削除

    # Solver 
    solver_settings = sim.SolverSettings
    solver_settings.Kernel = solver_settings.Kernel.enum.AXware

    # Update the materials with the new frequency parameters
    sim.UpdateAllMaterials() 

    # Update the grid with the new parameters
    sim.UpdateGrid()
    

    return sim


def AnalyzeSimulation(sim):
    # Create extractor for a given simulation output file
    results = sim.Results()

    print(results)

    # Em sensor extractor (元のoverall_field_sensorを流用)
    em_sensor_extractor = results[ 'Overall Field' ]
    em_sensor_extractor.FrequencySettings.ExtractedFrequency = u"All" # 全周波数で抽出
    document.AllAlgorithms.Add( em_sensor_extractor ) # S4Lドキュメントにアルゴリズムを追加

    # Adding a new StatisticsEvaluator for SAR
    # SAR(x,y,z,f0) を入力としてStatisticsEvaluatorを作成
    inputs_for_statistics = [em_sensor_extractor.Outputs["SAR(x,y,z,f0)"]]
    statistics_evaluator = analysis_core.StatisticsEvaluator(inputs=inputs_for_statistics)
    
    # 統計評価モードを設定
    statistics_evaluator.Mode = u"Value" # SAR値そのものを評価
    # 属性を更新
    statistics_evaluator.UpdateAttributes()
    # S4Lドキュメントにアルゴリズムを追加
    document.AllAlgorithms.Add( statistics_evaluator )

    # Adding a new DataTableHTMLViewer
    inputs_for_html_viewer = [statistics_evaluator.Outputs["SAR Statistics"]] # StatisticsEvaluatorの出力を入力とする
    data_table_html_viewer = viewers.DataTableHTMLViewer(inputs=inputs_for_html_viewer)
    
    # 属性を更新
    data_table_html_viewer.UpdateAttributes()
    # S4Lドキュメントにアルゴリズムを追加
    document.AllAlgorithms.Add(data_table_html_viewer)

def Run():
    import s4l_v1.document
    # s4l_v1.document.New() # 新規ドキュメントを作成する場合はコメントアウトを外す

    CreateModel() # 既存エンティティ前提のため、ここでは何もしない
    
    sim = CreateSimulation()
    
    
    s4l_v1.document.AllSimulations.Add(sim)
    sim.UpdateGrid()
    sim.CreateVoxels()  
    sim.RunSimulation(wait=True)  # True = wait until simulation has finished
	
    #sim = document.AllSimulations["EM_Py_Test"]
    AnalyzeSimulation(sim)

def main(data_path=None, project_dir=None):
    import sys
    import os
    print("Python ", sys.version)
    print("Running in ", os.getcwd(), "@", os.environ['COMPUTERNAME'])
    Run()

    """
        data_path = path to a folder that contains data for this simulation (e.g. model files)
        project_dir = path to a folder where this project and its results will be saved
    """
    
    # smashファイルを保存したい場合は以下を実行する
    """
    if project_dir is None:
        project_dir = os.path.expanduser(os.path.join('~', 'Documents', 's4l_python_tutorials') )
        
    if not os.path.exists(project_dir):
        os.makedirs(project_dir)

    fname = os.path.splitext(os.path.basename(_CFILE))[0] + '.smash'
    project_path = os.path.join(project_dir, fname)

    RunTutorial( project_path )
    """




if __name__ == '__main__':
    main()


# this is a test comment to check git commit
