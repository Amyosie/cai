from nicegui import ui

from functions import getDataFromSheet

def successWithBarcodePage(id_mumi) :
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
            ui.icon("check_circle", size="xs").style("padding:10px;border-radius:50%;background-color: #D5FBE4; color: #34A853;")
            ui.label("Absensi Berhasil").style("font-size:1.4em; font-weight: bold; ")
            
        ## Content
        with ui.column().style("""
                            width:100%;
                            padding:20px;
                            gap:10px;
                            align-items: center;
                            justify-content: center;
                            """) :
            ui.icon("check_circle", size="64px").style("color: #34A853;")
            ui.label("Absensi Berhasil!").style("font-size:1.2em; font-weight: bold; ")
            ui.label("Terima kasih telah melakukan absensi.").style("font-size:0.9em; color: gray; text-align:center; ")
            
            ui.button("Kembali ke Halaman Utama", on_click=lambda: ui.open('/')).style("""
                                                                                background-color: #34A853;
                                                                                color: white;
                                                                                padding: 10px 20px;
                                                                                border-radius: 5px;
                                                                                font-size: 1em;
                                                                                font-weight: bold;
                                                                                """)
            
            ui.label("ID Mumi: " + str(id_mumi)).style("font-size:0.9em; color: gray; text-align:center; margin-top:20px; ")

