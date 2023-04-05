from fastapi import FastAPI, Form, Response, UploadFile
from queue import Queue
from utils.utilities import PrintInfo, calculate_cost
from threading import Lock #RLock

app = FastAPI()

# secret: str = "$fJ@3&34ghaDF^2@"

file_queue: Queue = Queue(25)
sent_queue: Queue = Queue(25)
id: int = 1000
id_list: list = []
printed_id_list = []
id_lock: Lock = Lock()
print_lock: Lock = Lock()

@app.post("/uploadfile/")
async def queue_file(file: UploadFile,
                     no_of_copies: int = Form(default=1),
                     is_double_side: bool = Form(default=False),
                     is_colour_print: bool = Form(default=False),
                     page_count: int = Form(...)):

    with open(f"files/{file.filename}","wb") as f:
        f.write(file.file.read())

    file_path: str = f"./files/{file.filename}"

    print_info: PrintInfo = PrintInfo(file_path, no_of_copies, 
                                      is_double_side, 
                                      is_colour_print, 
                                      page_count)
    file_queue.put(print_info)

    local_id: int = -1

    id_lock.acquire(blocking=True)
    global id
    id = id + 1
    local_id = id
    id_list.append(id)
    id_lock.release()

    return {"info" : {
        "status" : "queued",
        "cost" : calculate_cost(print_info),
        "id" : local_id
    }}


@app.get("/download_pdf")
async def download_pdf():
    found: bool = False
    try:
        print_info: PrintInfo = file_queue.get(block=True, timeout=2)
        found = True
    except Exception:
        res = """{
            'info':'none'
        }"""
        found = False
        return Response(content=res, media_type="application/json", status_code=404)
    if found is True:
        sent_queue.put(print_info)

    with open(print_info.file_path, "rb") as file:
        pdf_file = file.read()
        file_name = file.name
        length = len(pdf_file)

    # Add headers
    headers = {
        "Content-Disposition": "attachment; filename=myfile.pdf",
        "Content-Type": "application/pdf",
        "Content-Length": str(length),
        "is_double_side": f"{print_info.is_double_side}",
        "is_colour_print": f"{print_info.is_colour_print}",
        "num_copies": f"{print_info.no_of_copies}",
        "file_name" : f"{file_name}"
    }
    print(file_name)

    # Add extra info in the response body
    return Response(content=pdf_file, headers=headers, media_type="application/pdf")

@app.get("/status")
async def get_status(file_id: int):
    id_lock.acquire(blocking=True)
    position: int = -1
    if file_id in id_list:
        position = id_list.index(file_id)
        id_lock.release()
    else:
        print_lock.acquire(blocking=True)
        if file_id in printed_id_list:
            print_lock.release()
            return {"status" : "printed"}
    if position == -1:
        return {"status": f"id = {file_id} not found"}
    return {
        "status" : "queued",
        "position" : f"{position + 1}"
    }

@app.get("/printed")
async def remove_id():
    sent_queue.get()
    print_lock.acquire(blocking=True)
    id_lock.acquire(blocking=True)
    printed_id_list.append(id_list[0])
    del id_list[0]
    id_lock.release()
    print_lock.release()
    return {"status" : "removed"}