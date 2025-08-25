from nicegui import ui, app
import asyncio

from formAbsen import formAbsenPage
from report import reportPage
from success import successPage
from successWithBarcode import successWithBarcodePage
from absenWitten import absenWrittenPage


@ui.page("/")
def formAbsen() :
    formAbsenPage()
    
@ui.page("/report")
def report() :
    reportPage()
    
@ui.page("/success")
def success() :
    successPage()

ui.run(title='Form Absensi', storage_secret="cai_2025", reconnect_timeout=12000000, reload=False) 
#ui.run(title='Form Absensi', storage_secret="cai_2025", reconnect_timeout=12000000) 