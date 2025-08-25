from nicegui import ui, app, events

from functions import getDataDesa, getDataKelompok, getDataMumi

def successPage() :
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
    
    if (app.storage.user['data']['mumi'] is None and app.storage.user['data']['dapukan'] is None) and (app.storage.user['data']['desa'] is None and app.storage.user['data']['kelompok'] is None) :
        ui.navigate.to("/")
    else :
    
        with ui.column().style("""
                            width:100%;
                            padding:20px;
                            gap:15px;
                            """) :
            with ui.column().style("""
                                width:100%;
                                align-items:center;
                                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                                border-radius:15px;
                                padding:20px;
                                gap:20px;
                                """) :
                ui.icon("check_circle", size="md", color="green").style("background-color:#D1FAE5;padding:10px;border-radius:50%")
                with ui.column().style("align-items:center;gap:5px") :
                    ui.label("Kehadiran Berhasil Disimpan!").style("font-size:1.3em; font-weight:bold")
                    ui.label("Alhamdulillah jaza kumullohu khoiro").style("font-size:0.8em; color:#4B5563")
                    
            with ui.column().style("""
                                width:100%;
                                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                                border-radius:15px;
                                padding:20px;
                                gap:10px;
                                """) :
                with ui.row().style("gap:10px") :
                    ui.icon("description", size="xs", color="#2563EB").style("background-color:#DBEAFE;padding:8px;border-radius:50%")
                    ui.label("Informasi Kehadiran").style("font-size:1em; font-weight:bold; align-self:center")
                    
                with ui.row().style("""
                                    width:100%;
                                    border-radius:10px;
                                    border:1px solid grey;
                                    padding:10px;
                                    background-color:#E2FBE8;
                                    margin-top:15px;
                                    """) :
                    ui.icon("person", size="xs", color="#2B6536").style("align-self:center;padding:5px;border-radius:50%;background-color:white")
                    with ui.column().style("gap:0") :
                        ui.label("Nama Peserta").style("font-size:0.8em; color:#6B7280")
                        ui.label(app.storage.user['data']['mumi']).style("font-size:1em; font-weight:bold")
                    ui.label(app.storage.user['data']['dapukan']).style("font-size:0.8em; color:#6B7280; margin-left:auto;font-weight:bold")
                        
                with ui.row().style("""
                                    width:100%;
                                    border-radius:10px;
                                    border:1px solid grey;
                                    padding:10px;
                                    """) :
                    ui.icon("location_on", size="xs", color="#0D3AAB").style("align-self:center;padding:5px;border-radius:50%;background-color:#ECF5FE")
                    with ui.column().style("gap:0") :
                        ui.label("Desa").style("font-size:0.8em; color:#6B7280")
                        ui.label(app.storage.user['data']['desa']).style("font-size:1em; font-weight:bold")
                        
                with ui.row().style("""
                                    width:100%;
                                    border-radius:10px;
                                    border:1px solid grey;
                                    padding:10px;
                                    """) :
                    ui.icon("group", size="xs", color="#922FF4").style("align-self:center;padding:5px;border-radius:50%;background-color:#F9F4FE")
                    with ui.column().style("gap:0") :
                        ui.label("Kelompok").style("font-size:0.8em; color:#6B7280")
                        ui.label(app.storage.user['data']['kelompok']).style("font-size:1em; font-weight:bold")
                        
                with ui.row().style("""
                                    width:100%;
                                    border-radius:10px;
                                    border:1px solid grey;
                                    padding:10px;
                                    """) :
                    ui.icon("calendar_month", size="xs", color="#D7922C").style("align-self:center;padding:5px;border-radius:50%;background-color:#FEFBE6")
                    with ui.column().style("gap:0") :
                        ui.label("Waktu Absen").style("font-size:0.8em; color:#6B7280")
                        ui.label(f"{app.storage.user['data']['hari']}, {app.storage.user['data']['absensi_tanggal']}").style("font-size:1em; font-weight:bold")
                        ui.label(f"Pukul {app.storage.user['data']['absensi_jam']}").style("font-size:0.8em")
                        
            with ui.column().style("""
                                width:100%;
                                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                                align-items:center;
                                border-radius:15px;
                                padding:20px;
                                gap:5px;
                                """) :
                ui.label("Status Absensi").style("font-size:0.8em;color:#4B5563")
                ui.label("Tercatat").style("font-size:1.5em; font-weight:bold; color:#16A34A")  
                ui.label("Data Berhasil disimpan didalam sistem").style("font-size:0.8em;color:#4B5563") 
                
        