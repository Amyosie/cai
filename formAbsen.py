from nicegui import ui, app, events
from datetime import datetime
import pandas as pd


from functions import getDataDesa, getDataKelompok, getDataMumi, submitKehadiran, getDataFromSheet

def formAbsenPage() :
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
    
    app.storage.user['data'] = {
        "desa": None,
        "kelompok": None,
        "mumi": None,
        "dapukan": None,
        "absensi_tanggal": None,
        "absensi_jam": None,
    }
    
    now = datetime.now()
    day_number = now.day
    day_name = now.strftime("%A")
    formatted_date = now.strftime("%d %B %Y")
    
    try :
        dataDesasheets = getDataDesa()
        listDesa = list(dataDesasheets["desa"])
        dataKelompoksheets = getDataKelompok()
        dataMumisheets = getDataMumi()
    except Exception as e :
        print(f"Error fetching data from sheets: {e}")
        dataDesasheets = pd.DataFrame(columns=["id_desa", "desa"])
        listDesa = []
        dataKelompoksheets = pd.DataFrame(columns=["id_kelompok", "kelompok", "id_desa"])
        dataMumisheets = pd.DataFrame(columns=["id_mumi", "nama", "id_kelompok", "dapukan"])

    def getFilteredKelompok(desa, getkelompok, ds) :
        if desa != None :
            idDs = list(dataDesasheets[dataDesasheets["desa"] == desa]["id_desa"])
            getKl = dataKelompoksheets[dataKelompoksheets["id_desa"] == idDs[0]]
            getKl = list(getKl["kelompok"])
            getkelompok.set_options(getKl)
            getkelompok.enabled = True
            ds.set_text(desa)
            app.storage.user['data']['desa'] = desa
        else :
            getkelompok.value = None
            ds.set_text("") 
            getkelompok.enabled = False
            
    def getFilteredMumi(kelompok, getMumi, kl, contKehadiranMumi) :
        if kelompok != None :
            idKl = list(dataKelompoksheets[dataKelompoksheets["kelompok"] == kelompok]["id_kelompok"])
            getMm = dataMumisheets[(dataMumisheets["id_kelompok"] == idKl[0]) & (dataMumisheets["nama"] != "")]
            getMm = list(getMm["nama"])
            getMumi.set_options(getMm)
            getMumi.enabled = True
            kl.set_text(kelompok)
            contKehadiranMumi.visible = True
            app.storage.user['data']['kelompok'] = kelompok
        else :  
            getMumi.value = None
            kl.set_text("")
            getMumi.enabled = False
            contKehadiranMumi.visible = False
            
    def getAbsen(mumi, nameMumi, dapukan, detailKehadiran, buttonHadir) :
        if mumi != None :
            nameMumi.set_text(mumi)
            getDapukan = dataMumisheets[dataMumisheets["nama"] == mumi]["dapukan"].values[0]
            dapukan.set_text(f"{getDapukan}")
            detailKehadiran.visible = True
            buttonHadir.visible = True
            app.storage.user['data']['mumi'] = mumi
            app.storage.user['data']['dapukan'] = getDapukan
            app.storage.user['data']['hari'] = day_name
            app.storage.user['data']['absensi_tanggal'] = formatted_date
            app.storage.user['data']['absensi_jam'] = now.strftime("%H:%M")
        else :
            nameMumi.set_text("")
            detailKehadiran.visible = False
            buttonHadir.visible = False
            
    
        
    with ui.column().style("""
                           width:100%;
                           padding:20px;
                           gap:10px;
                        """) :
        with ui.row().style("""
                            width:100%;
                            padding:20px;
                            border-radius: 10px;
                            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                            gap:10px;
                            """) :
            ui.icon("fact_check", size="sm", color="#273FB3").style("align-self:center;padding:10px;border-radius:50%;background-color:#DEEAFC")
            with ui.column().style("""
                                   """) :
                with ui.column().style("gap:0") :
                    ui.label("Form Absensi").style("font-size:1.5em; font-weight:bold;")
                    ui.label(f"{day_name}, {formatted_date}").style("font-size:0.9em")
        with ui.column().style("""
                                width:100%;
                                background-color:white;
                                border-radius:20px;
                                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                                padding : 20px 10px 20px 10px;
                                gap:15px;
                                """) :
            
            with ui.column().style("width:100%;gap:0") :
                
                with ui.row().style("margin-bottom:20px;gap:5") :
                    ui.icon("location_on", size="sm", color="#2B6536").style("align-self:center;padding:5px;border-radius:50%;background-color:#D5FBE4")
                    ui.label("Informasi Sambung").style("font-size:1em;font-weight:bold; align-self:center")
                    
                ui.label("Pilih Desa").style("font-size:0.9em")
                getDesa = ui.select(options=listDesa, 
                                    label="Desa", 
                                    clearable=True,
                                    on_change= lambda e : getFilteredKelompok(e.value, getkelompok, ds)).props("standout dense clearable").style("width:100%;")
                
            with ui.column().style("width:100%;gap:0") :
                ui.label("Pilih Kelompok").style("font-size:0.9em")
                getkelompok = ui.select(options=listDesa, 
                                        label="Kelompok",
                                        clearable=True,
                                        on_change= lambda e : getFilteredMumi(e.value, getMumi, kl, contKehadiranMumi)
                                        ).props("standout dense clearable").style("width:100%;")
                getkelompok.enabled = False
        
        contKehadiranMumi = ui.column()
        contKehadiranMumi.visible = False
        with contKehadiranMumi.style("""
                               width:100%;
                                background-color:white;
                                border-radius:20px;
                                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                                padding : 20px 15px 20px 15px;
                                gap:15px;
                               """) :
            with ui.row().style("width:100%;gap:10px") :
                ui.icon("person", size="sm", color="#8E28F3").style("align-self:center;padding:5px;border-radius:50%;background-color:#F9F4FE")
                ui.label("Pilih Nama").style("font-size:1em; align-self:center;font-weight:bold")
                    
            with ui.column().style("width:100%;gap:0") :
                ui.label("Pilih Nama Peserta").style("font-size:0.9em")
                getMumi = ui.select(options=listDesa, 
                                        label="Pilih Nama...",
                                        with_input = True,
                                        clearable=True,
                                        on_change = lambda e : getAbsen(e.value, nameMumi, dapukan, detailKehadiran, buttonHadir),
                                        ).props("standout dense clearable").style("width:100%;")
                
                getMumi.enabled = False
                
        detailKehadiran = ui.column()
        detailKehadiran.visible = False
            
        with detailKehadiran.style("""
                                   width:100%;
                                        background-color:white;
                                        border-radius:20px;
                                        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                                        padding : 20px 15px 20px 15px;
                                        gap:15px;
                                   """) :
                with ui.row().style("gap:5px") :
                    ui.icon("contact_page", size="xs")
                    ui.label("Detail Kehadiran").style("font-size:1em; font-weight:bold")
                    
                nameMumi = ui.label("Nama Peserta").style("font-size:1.5em; font-weight:bold;align-self:center")
                dapukan = ui.label("KMM Kelompok").style("font-size:1em; font-weight:bold;align-self:center")
                with ui.row().style("flex:1;align-items:end;align-self:center;gap:2px") :
                    ds = ui.label("Desa").style("font-size:0.9em")
                    ui.label("-")
                    kl = ui.label("Kelompok").style("font-size:0.9em")
                ui.label("Siap mengikuti kegiatan pengajian hari ini.").style("font-size:0.9em; align-self:center")   
        
        buttonHadir =  ui.row()
        buttonHadir.visible = False
        with buttonHadir.style("""
                            width:100%;
                            padding: 10px 15px 10px 15px;
                            border-radius:5px;
                            background-color: #D5FBE4;
                            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                            align-items:center;
                            justify-content:center;
                            margin-top:20px;
                            gap:3px
                            """).on("click", lambda : submitKehadiran(getMumi, loadingView, alreadyAbsen, textAbsen)) :
            ui.icon("assignment", size="xs")
            ui.label("Submit Kehadiran")
            
    loadingView =  ui.column()
    loadingView.visible = False
            
    with loadingView.style("""
                        position:absolute;
                        top:0;
                        width:100%;
                        height:100vh;
                        background-color: rgba(255, 255, 255, 0.4);
                        -webkit-backdrop-filter: blur(5px);
                        backdrop-filter: blur(5px);
                        align-self:center;
                        justify-content: center;
                        """) :
        ui.spinner("dots", size="xl").style("align-self:center")
        ui.label("Data anda sendang diproses...").style("align-self:center")
    
    alreadyAbsen =  ui.column()
    alreadyAbsen.visible = False 
    
    with alreadyAbsen.style("""
                    position:absolute;
                    top:0;
                    width:100%;
                    height:100vh;
                    background-color: rgba(255, 255, 255, 0.4);
                    -webkit-backdrop-filter: blur(5px);
                    backdrop-filter: blur(5px);
                    align-self:center;
                    justify-content: center;
                    """) :
        textAbsen = ui.label(f"Anda sudah melakukan absen untuk hari ini...").style("font-size: 2em; font-weight: bold;text-align: center;align-self:center")
        ui.label(f"Alhamdulillahi jaza kumullohu khoiro").style("font-size: 1.5em; font-weight: bold;text-align: center;align-self:center")