from fastapi import FastAPI, Response, Query, HTTPException, Header, UploadFile, File, Form, Body
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient
from typing import List, Dict
from datetime import datetime
import json
from json import dumps, loads

app = FastAPI()
client = MongoClient("mongodb://localhost:27017/")
db = client["MES"]
collection = db["production_record"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)
class InspectionDetail(BaseModel):
    inspectionID: str
    status: str
    remarks: str

class RawMaterial(BaseModel):
    rawMaterial: str
    qtyRequired: int
    warehouseEntry: datetime
    warehouseExit: datetime

class Record(BaseModel):
    batchId: str
    inspectionDate: datetime
    inspectorName: str
    qty: int
    defectQty: int
    productionLine: str
    machine: str
    inspectionStatus: str
    inspectionRemarks: str
    inspectionDetails: List[InspectionDetail]
    productionStart: datetime
    productionEnd: datetime
    productionStatus: str
    productionRemarks: str
    rawMaterials: List[RawMaterial]
    productEntry: datetime
    productExit: datetime
    deliveryDate: datetime
    status: str
    remarks: str

# Fetch all records endpoint
@app.get("/get_record", response_model=List[Record])
async def get_record():
    records = collection.find()  # Query all products in the collection
    records_list = []
    for record in records:
        record["_id"] = str(record["_id"])  # Convert the _id field to a string
        records_list.append(record)
    return records_list

# Update Production Records
@app.put("/update_record/{batch_id}")
async def update_record(batch_id: str, record: Record):
    try:
        record_dict = record.dict() 
        # Update the record in MongoDB
        result = collection.update_one(
            {"batchId": batch_id},  # Match the batchId
            {"$set": record_dict}   # Update the document
        )

        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Record not found")

        return {"message": "Record updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/add_record")
async def add_record(record: Record):
    try:
        # Insert the new record into MongoDB
        result = await collection.insert_one(record.dict())

        # Return the inserted ID
        return {"message": "Record added successfully", "record_id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add record: {str(e)}")
    
@app.delete("/delete_record/{batch_id}")
async def delete_record(batch_id: str):
    try:
        # Delete the record from the database
        result = collection.delete_one({"batchId": batch_id})

        # If no record was matched, return an error
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Record not found")

        # Return a success message
        return {"message": "Record deleted successfully"}
    except Exception as e:
        # If there was any error, raise an internal server error
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__api__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)