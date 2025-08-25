from nicegui import ui
from datetime import datetime

from functions import getDataFromSheet

def absenWrittenPage() :
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
    
    todayDate = datetime.now().strftime("%Y-%m-%d")
    
    sesiSatuStart = datetime.strptime(f"{todayDate} 06:00:00", "%Y-%m-%d %H:%M:%S")
    sesiSatuEnd = datetime.strptime(f"{todayDate} 12:00:00", "%Y-%m-%d %H:%M:%S")
    
    sesiDuaStart = datetime.strptime(f"{todayDate} 12:30:00", "%Y-%m-%d %H:%M:%S")
    sesiDuaEnd = datetime.strptime(f"{todayDate} 17:00:00", "%Y-%m-%d %H:%M:%S")
    
    sesiTigaStart = datetime.strptime(f"{todayDate} 18:00:00", "%Y-%m-%d %H:%M:%S")
    sesiTigaEnd = datetime.strptime(f"{todayDate} 22:00:00", "%Y-%m-%d %H:%M:%S")
    
    tanggalAbsensi = datetime.now()
    
    if tanggalAbsensi > sesiSatuStart and tanggalAbsensi < sesiSatuEnd :
        sesi = "sesi 1"
    elif tanggalAbsensi > sesiDuaStart and tanggalAbsensi < sesiDuaEnd :
        sesi = "sesi 2"
    elif tanggalAbsensi > sesiTigaStart and tanggalAbsensi < sesiTigaEnd :
        sesi = "sesi 3"
    
    with ui.column().style("""
                           width: 100%;
                            height: 100vh;
                            align-items: center;
                            justify-content: center;
                           """) :
        ui.label(f"Anda sudah melakukan absen untuk {sesi} hari ini...").style("font-size: 2em; font-weight: bold;text-align: center")
        ui.label(f"Alhamdulillahi jaza kumullohu khoiro").style("font-size: 1.5em; font-weight: bold;text-align: center")