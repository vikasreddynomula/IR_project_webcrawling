import subprocess
import requests
from nicegui import ui
from processor import app

base_url = "http://127.0.0.1:5000"
search_results = {}
process_started = True

if process_started:
    subprocess.Popen(["python", "processor.py"])
    process_started = False

def on_start():
    response = requests.get(f"{base_url}/init")

    if response.status_code == 200:
        print("Flask server initialized successfully.")
        ui.notify(response.json()['message'], type='positive')
    else:
        print("Error:", response.status_code, response.text)
        ui.notify(response.json()['error'], type='negative')

def on_search_click():
    search_text = search_query.value
    url = f"{base_url}/process_query"
    data = {"query": search_text}
    response = requests.post(url, json=data)

    if response.status_code == 200:
        global search_results
        search_results = response.json()['results']
    
        search_list.refresh()
        ui.notify(response.json()['message'], type='positive',color='black')
    else:
        print("Error:", response.status_code, response.text)
        ui.notify(response.json()['error'], type='negative',color='black')

@ui.refreshable
def search_list():
    with ui.list().classes('self.center'):
        for item in search_results:
            ui.item(f"{item['article']}", on_click=lambda x: ui.navigate().to(item['link'])).style('color: blue;')
            ui.separator()

ui.button("Load Data", on_click=on_start).classes('self-center').props("color=green")

with ui.row().classes('self-center'):
    search_query = ui.input(placeholder='Type Here').props(
        'wide-input outlined dense self-center').classes('w-96')
    ui.button("Go", on_click=on_search_click).props("color=green")

search_list()

ui.run()
