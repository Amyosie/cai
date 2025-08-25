from nicegui import ui

from functions import getDataFromSheet

def reportPage() :
    ui.add_head_html('''
    <style>
        body, html {
            margin: 0;
            padding: 0;
            height: 100%;
            background-color: #F9FAFB;
        }
        .nicegui-content {
            margin: 0;
            padding: 0;
        }
        .no-padding-margin{
            margin: 0 !important;
            padding: 0;
        }
    </style>
    ''')
    
    data = getDataFromSheet("absensi")
    
    with ui.column().style("""
                        width:100%;
                        height:100vh;
                        gap:0;
                        """) :
        ## header
        with ui.row().style("""
                            width:100%;
                            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                            padding : 15px;
                            align-items: center;
                            """) :
            ui.icon("insert_chart", size="xs").style("padding:10px;border-radius:50%;background-color: #D5FBE4")
            ui.label("Laporan Absensi").style("font-size:1.4em; font-weight: bold; ")
            
        ## Content
        dataMumi = getDataFromSheet("mumi")['id_mumi'].nunique()
        percentageMumi = (len(data) / dataMumi) * 100 if dataMumi > 0 else 0
        percentageMumi = round(percentageMumi, 2)
        with ui.column().style("""
                            width:100%;
                            padding:20px;
                            gap:10px;
                            """) :
            with ui.column().style("gap:0") :
                ui.label("Data Absensi Kegiatan CAI").style("font-size:1.2em; font-weight: bold; ")
                ui.label("Berikut adalah data absensi kegiatan CAI yang telah tercatat.").style("font-size:0.9em; color: gray; ")
            
            ## Total Kehadiran
            with ui.row().style("""
                                width:100%;
                                padding:20px 15px 20px 20px;
                                background-color: white;
                                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                                border-radius:10px;
                                gap: 25px;
                                """) :  
                
                ui.icon("people", size="xs", color="#2B6536").style("padding:10px;border-radius:50%;background-color: #D5FBE4; align-self: center;")
                with ui.column().style("gap:0") :
                    ui.label("Total Kehadiran").style("font-size:0.9em; color: gray; ")
                    ui.label(f"{len(data)} Peserta").style("font-size:1.2em; font-weight: bold; ")
                with ui.column().style("flex: 1; gap:0") :
                    ui.label(f"{percentageMumi}%").style(f"font-size:1em; align-self: flex-end; font-weight: bold;background-color: {'#D5FBE4' if percentageMumi > 50 else '#FAEBF3' };padding:5px; border-radius: 5px;")
                    ui.label(f"{dataMumi} perserta").style("font-size:0.9em; color: gray; align-self: flex-end")
                    
            ## Kehadiran Desa
            desa = getDataFromSheet("desa")
            dataDesa = desa['id_desa'].nunique()
            TotalKehadiranDesa = data['id_desa'].nunique()
            percentageDesa = (TotalKehadiranDesa / dataDesa) * 100 if dataDesa > 0 else 0
            percentageDesa = round(percentageDesa, 2)
            with ui.row().style("""
                                width:100%;
                                padding:20px 15px 20px 20px;
                                background-color: white;
                                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                                border-radius:10px;
                                gap: 25px;
                                """) :  
                
                ui.icon("grain", size="xs", color="#273FB3").style("padding:10px;border-radius:50%;background-color: #DEEAFC; align-self: center;")
                with ui.column().style("gap:0") :
                    ui.label("Kehadiran Desa").style("font-size:0.9em; color: gray; ")
                    ui.label(f"{TotalKehadiranDesa} Desa").style("font-size:1.2em; font-weight: bold; ")
                    
                with ui.column().style("flex: 1; gap:0") :
                    ui.label(f"{percentageDesa}%").style(f"font-size:1em; align-self: flex-end; font-weight: bold;background-color: {'#D5FBE4' if percentageDesa > 50 else '#FAEBF3' };padding:5px; border-radius: 5px;")
                    ui.label(f"{dataDesa} desa").style("font-size:0.9em; color: gray; align-self: flex-end") 
                    
            ## Kehadiran Kelompok
            dataKelompok = getDataFromSheet("kelompok")['id_kelompok'].nunique()
            TotalKehadiranKelompok = data['id_kelompok'].nunique()
            percentageKelompok = (TotalKehadiranKelompok / dataKelompok) * 100 if dataKelompok > 0 else 0
            percentageKelompok = round(percentageKelompok, 2)
            with ui.row().style("""
                                width:100%;
                                padding:20px 15px 20px 20px;
                                background-color: white;
                                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                                border-radius:10px;
                                gap: 25px;
                                """) :  
                
                ui.icon("hub", size="xs", color="#8E28F3").style("padding:10px;border-radius:50%;background-color: #F9F4FE; align-self: center;")
                with ui.column().style("gap:0") :
                    ui.label("Kehadiran Kelompok").style("font-size:0.9em; color: gray; ")
                    ui.label(f"{TotalKehadiranKelompok} Kelompok").style("font-size:1.2em; font-weight: bold; ")
                with ui.column().style("flex: 1; gap:0") :
                    ui.label(f"{percentageKelompok}%").style(f"font-size:1em; align-self: flex-end; font-weight: bold;background-color: {'#D5FBE4' if percentageKelompok > 50 else '#FAEBF3' };padding:5px; border-radius: 5px;")
                    ui.label(f"{dataKelompok} kelompok").style("font-size:0.9em; color: gray; align-self: flex-end") 
                    
            ## Chrat Kehadiran Desa
            with ui.column().style("""
                                width:100%;
                                padding:20px;
                                background-color: white;
                                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                                border-radius:10px;
                                gap:0;
                                """) :
                ui.label("Chart Kehadiran Desa").style("font-size:1em; font-weight: bold; ")
                ui.echart({
                    'xAxis': {'type': 'category', 'data': desa["id_desa"].tolist()},
                    'yAxis': {'type': 'value'},
                    'series': [{'type': 'line', 'data': [230, 224, 218, 135, 147, 260, 300, 280, 250]}],
                }).style('width: 100%')
        
        
    