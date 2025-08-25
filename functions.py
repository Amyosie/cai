import pandas as pd
from sqlalchemy import create_engine
import psycopg2
from nicegui import ui, app, events
import datetime
import asyncio
from datetime import datetime

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint as pp

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("project-cai-468709-42942b9782c3.json",scope)
client = gspread.authorize(creds)

username = "postgres.hmfjkskmstnsbusphgvb"
password = "Amyosie%40597"
url = f"postgresql://{username}:{password}@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres"


def engineSupabase() :
    db_string = url

    db = create_engine(db_string)
    
    return db

def getDataDesa() :
    query = "select * from desa"
    data = pd.read_sql(query, engineSupabase())
    return data

def getDataKelompok() :
    query = "select * from kelompok"
    data = pd.read_sql(query, engineSupabase())
    return data

def getDataMumi() :
    query = "select * from mumi"
    data = pd.read_sql(query, engineSupabase())
    return data
    
def getDataAbsensi() :
    query = "select * from absensi"
    data = pd.read_sql(query, engineSupabase())
    return data

def getDataFromSheet(sheetName) :
    try:
        sheet = client.open("Data CAI").worksheet(sheetName)
        data = pd.DataFrame(sheet.get_all_records())
        return data
    except Exception as e:
        print(f"Error accessing sheet {sheetName}: {e}")
        return pd.DataFrame()
    
async def submitKehadiran(getMumi, loadingView, alreadyAbsen, textAbsen) :
    loadingView.visible = True
    
    todayDate = datetime.now().strftime("%Y-%m-%d")
    
    sesiSatuStart = datetime.strptime(f"{todayDate} 06:00:00", "%Y-%m-%d %H:%M:%S")
    sesiSatuEnd = datetime.strptime(f"{todayDate} 12:00:00", "%Y-%m-%d %H:%M:%S")
    
    sesiDuaStart = datetime.strptime(f"{todayDate} 12:30:00", "%Y-%m-%d %H:%M:%S")
    sesiDuaEnd = datetime.strptime(f"{todayDate} 17:00:00", "%Y-%m-%d %H:%M:%S")
    
    sesiTigaStart = datetime.strptime(f"{todayDate} 18:00:00", "%Y-%m-%d %H:%M:%S")
    sesiTigaEnd = datetime.strptime(f"{todayDate} 22:00:00", "%Y-%m-%d %H:%M:%S")
    
    await asyncio.sleep(1)
    
    tanggalAbsensi = datetime.now()
    
    def inputData(sesi) :
        
        dataMumi = getDataMumi()
        dataMumi = dataMumi[dataMumi["nama"] == getMumi.value].to_dict('records')[0]
        sheetAbsensi = client.open("Data CAI").worksheet("absensi")
            
        
        dataAbsensi = getDataAbsensi()
        
        
        if len(dataAbsensi) != 0 :
            dataAbsensi = dataAbsensi[(dataAbsensi["id_mumi"] == dataMumi["id_mumi"]) & (dataAbsensi["tanggal_jam"].str.contains(tanggalAbsensi.strftime("%Y-%m-%d"))) & (dataAbsensi["sesi"] == sesi)]
    
            if not dataAbsensi.empty :
                loadingView.visible = False
                alreadyAbsen.visible = True
                textAbsen.set_text(f"Anda sudah melakukan absen untuk {sesi} hari ini...")
                return
            
            insertData = pd.DataFrame(columns=["id_desa", "id_kelompok", "id_mumi", "nama", "sesi", "tanggal_jam"], data=[( dataMumi["id_desa"], dataMumi["id_kelompok"], dataMumi["id_mumi"], dataMumi["nama"], sesi, tanggalAbsensi.strftime("%Y-%m-%d %H:%M:%S"))])  
                
            insertRow = [dataMumi["id_desa"], dataMumi["id_kelompok"], dataMumi["id_mumi"], dataMumi["nama"], sesi, tanggalAbsensi.strftime("%Y-%m-%d %H:%M:%S")]
            
            sheetAbsensi.append_row(insertRow)
            
            insertData.to_sql('absensi', engineSupabase(), if_exists='append', index=False)
            
            loadingView.visible = False
            ui.navigate.to("/success")
            
        else :
        
            try :
                insertData = pd.DataFrame(columns=["id_desa", "id_kelompok", "id_mumi", "nama", "sesi", "tanggal_jam"], data=[( dataMumi["id_desa"], dataMumi["id_kelompok"], dataMumi["id_mumi"], dataMumi["nama"], sesi, tanggalAbsensi.strftime("%Y-%m-%d %H:%M:%S"))])  
                
                insertData.to_sql('absensi', engineSupabase(), if_exists='append', index=False)
                
                insertRow = [dataMumi["id_desa"], dataMumi["id_kelompok"], dataMumi["id_mumi"], dataMumi["nama"], sesi, tanggalAbsensi.strftime("%Y-%m-%d %H:%M:%S")]
            
                sheetAbsensi.append_row(insertRow)
            except Exception as e :
                print(f"Error appending row: {e}")
            
            loadingView.visible = False
            ui.navigate.to("/success")
        
    # if tanggalAbsensi > sesiSatuStart and tanggalAbsensi < sesiSatuEnd :
    #     inputData("sesi 1")
    # elif tanggalAbsensi > sesiDuaStart and tanggalAbsensi < sesiDuaEnd :
    #     inputData("sesi 2")
    # elif tanggalAbsensi > sesiTigaStart and tanggalAbsensi < sesiTigaEnd :
    #     inputData("sesi 3")
    
    inputData("sesi 1")
    
    
    # lat = "-6.22"
    # long = "107.7"
    
    # result = await ui.run_javascript('''
    #     return await new Promise((resolve, reject) => {
    #         if ("geolocation" in navigator) {
    #             navigator.geolocation.getCurrentPosition(
    #                 position => resolve({
    #                     lat: position.coords.latitude,
    #                     lon: position.coords.longitude,
    #                 }),
    #                 error => reject(error),
    #             );
    #         } else {
    #             reject("Geolocation is not supported by this browser.");
    #         }
    #     });
    # ''', timeout=10)
    # if lat == str(result["lat"])[:9] and long == str(result["long"])[:9]  :
    #     ui.notify("Berhasil Absen")
    # else :
    #     ui.notify("Anda bukan dilokasi pengajian")
        
    # query = f"""
    # insert into absensi ({", ".join(allColumn)}) values ('{len(dataAbsensi) + 1}', '{dataMumi["id_desa"]}', '{dataMumi["id_kelompok"]}', '{dataMumi["id_mumi"]}', '{dataMumi["nama"]}', '{tanggalAbsensi}')
    # """