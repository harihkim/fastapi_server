# from fastapi import FastAPI, UploadFile
# from queue import Queue
# from utils.utilities import PrintInfo, calculate_cost
# from pydantic import BaseModel

# class FileInfo(BaseModel):
#     no_of_copies: int
#     is_double_side: bool
#     page_count: int

# app = FastAPI()

# secret: str = "$fJ@3&34ghaDF^2@"

# file_queue :Queue = Queue(25)

# # @app.post("/uploadfile/")
# # async def queue_file(file: UploadFile, info: FileInfo):
# #     # print(file.filename, file.content_type,"hhhh")
# #     print_info = PrintInfo(file, info.no_of_copies, info.is_double_side,info.page_count)
# #     file_queue.put(print_info)
# #     return {"info" : {
# #         "status" : "queued",
# #         "cost" : print_info.calculate_cost()
# #     }}

# @app.post("/uploadfile/")
# async def queue_file(file: UploadFile):
#     # print(file.filename, file.content_type,"hhhh")
#     print_info: PrintInfo = PrintInfo(file, 5, False, 1)
#     file_queue.put(print_info)
#     return {"info" : {
#         "status" : "queued",
#         "cost" : calculate_cost(print_info)
#     }}

# @app.get("/getFile")
# async def sendF(secrt: str):
#     if file_queue.qsize == 0:
#         return {"info" : {
#         "status" : "check later",
#         "file" : None
#     }}

#     res: PrintInfo = file_queue.get(block=True)

#     return {"info" : {
#         "status" : "sent file",
#         "file" : res
#     }}

# @app.get("/giveFile")
# def send_file():
#     # Read file content
#     print_info:PrintInfo  = file_queue.get(block=True)
#     file_content = print_info.file.file.read()

#     # Set response headers for binary file
#     # headers = {
#     #     "Content-Disposition": f"attachment; filename={print_info.file.filename}",
#     #     "Content-Type": print_info.file.content_type,
#     # }

#     # Return JSON response with metadata and binary file as response content
#     return {
#         "metadata": {
#             "file_name": print_info.file.filename,
#             "no_copies": print_info.no_of_copies
#         },
#         "file": file_content.decode("ISO-8859-1")
#     }
