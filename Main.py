import io
import os
import fitz
import uvicorn
import time
from PIL import Image
from fastapi import FastAPI,UploadFile, HTTPException,responses

#* Brightness Threshold :
Brightness_Threshold=250

#* Diffrence Channel Threshold : 
Diff_Threshold=10

app = FastAPI(title="Background Color Checker")

@app.get("/",include_in_schema=False)
async def Home():
    Redirect = responses.RedirectResponse(url='/docs')
    return Redirect

#* Colored Section :
@app.post("/Check_Colored (Image)")
async def Check_Colored(Image_File:UploadFile):
    try:
        #* Loading Image : 
        Content =await Image_File.read() 
        Img = Image.open(io.BytesIO(Content))

        #* Convert to RGB :
        Img=Img.convert('RGB')

        #* Find Max Density :
        Color=max(Img.getcolors(Img.size[0]*Img.size[1]))
        Color=Color[1][0:]

        #* Mean Of 3 Channels :
        Mean =sum(Color)/3

        #* Check With Threshold Limit :
        if(Mean >=Brightness_Threshold):
            if(abs(max(Color)-min(Color))>=Diff_Threshold):
                Result= True
            else:
                Result= False 
        else:
            Result= True  
             
    except Exception:
        raise HTTPException(status_code=500, detail='Something went wrong')
    
    return {"Result": f" {Result} - Background Color(RGB): {Color}"}

#* GrayScale Section :
@app.post("/Check_GrayScale",include_in_schema=False)
async def Check_GrayScale(Image_File:UploadFile):
    try:

        #* Loading Image : 
        Content =await Image_File.read() 
        Img = Image.open(io.BytesIO(Content))

        #* Convert to GrayScale :
        Img=Img.convert('L')

        #* Find Max Density :
        Color=max(Img.getcolors(Img.size[0]*Img.size[1]))
        Color=Color[1]

        #* Check With Threshold Limit :
        if(Color<=Brightness_Threshold):
            Result=True
        else:
            Result=False

    except Exception:
        raise HTTPException(status_code=500, detail='Something went wrong')
    
    return {"Success": f"Result :{Result} - Background Color(GrayScale): {Color}"}

#* Colored Pdf (Single Page):
@app.post("/Check_Colored (PDF - Single Page)")
async def Check_Colored_PDF(Pdf : UploadFile,Page : int=0):
    try:
        #* Load Pdf File :
        Content =await Pdf.read() 
        Document = fitz.open(stream=Content)
        
        #* Select Desired Page ( Default == 0 ) :
        Selected_Page = Document.load_page(Page)

        #* Convert to Image :
        Pix = Selected_Page.get_pixmap()
        Pix.save("Result.jpg")
        Document.close()

        #* Loading Image : 
        Img = Image.open("Result.jpg")

        #* Convert to RGB :
        Img=Img.convert('RGB')

        #* Find Max Density :
        Color=max(Img.getcolors(Img.size[0]*Img.size[1]))
        Color=Color[1][0:]

        #* Mean Of 3 Channel :
        Mean =sum(Color)/3

        #* Check With Threshold Limit :
        if(Mean >=Brightness_Threshold):
            if(abs(max(Color)-min(Color))>=Diff_Threshold):
                Result= True
            else:
                Result= False 
        else:
            Result= True    

        #* Remove Temp Image :
        os.remove("Result.jpg") 

    except Exception:
        raise HTTPException(status_code=500, detail='Something went wrong')
    
    return {" Result": f" {Result} - Background Color(RGB): {Color}"}
    
#* Colored Pdf (Full Page):
@app.post("/Check_Colored (PDF - Full Page)")
async def Check_Colored_PDF(Pdf : UploadFile):
    try:
        #* Load Pdf File :
        Content =await Pdf.read() 
        Document = fitz.open(stream=Content)
        
        Result_Dict={}
        Start_time=time.time()
        Number_of_pages=Document.page_count
        for i in range(Document.page_count):
            #* Select Desired Page ( Default == 0 ) :
            Selected_Page = Document.load_page(i)

            #* Convert to Image :
            Pix = Selected_Page.get_pixmap()
            Pix.save("Result.jpg")

            #* Loading Image : 
            Img = Image.open("Result.jpg")

            #* Convert to RGB :
            Img=Img.convert('RGB')

            #* Find Max Density :
            Color=max(Img.getcolors(Img.size[0]*Img.size[1]))
            Color=Color[1][0:]

            #* Mean Of 3 Channel :
            Mean =sum(Color)/3

            #* Check With Threshold Limit :
            if(Mean >=Brightness_Threshold):
                if(abs(max(Color)-min(Color))>=Diff_Threshold):
                    Result= True
                else:
                    Result= False 
            else:
                Result= True  

            #* Check Result :
            if(Result == True):

                Result_Dict[i]=Result

        Done=time.time()
        Result_Time=round(Done-Start_time)
        #* Remove Temp Image :
        os.remove("Result.jpg") 

    except Exception:
        raise HTTPException(status_code=500, detail='Something went wrong')
    
    return {"Result Time":f"{Result_Time} s","Number Of Pages":f"{Number_of_pages}","Colored Pages": f"{Result_Dict}"}

#* GrayScale Pdf Section :
@app.post("/Check_GrayScale (PDF)" , include_in_schema=False)
async def Check_GrayScale_PDF(Pdf : UploadFile,Page : int=0):
    try:
        #* Load Pdf File :
        Content =await Pdf.read() 
        Document = fitz.open(stream=Content)
        
        #* Select Desired Page ( Default == 0 ) :
        Selected_Page = Document.load_page(Page)

        #* Convert to Image :
        Pix = Selected_Page.get_pixmap()
        Pix.save("Result.jpg")
        Document.close()

        #* Loading Image : 
        Img = Image.open("Result.jpg")

        #* Convert to GrayScale :
        Img=Img.convert('L')

        #* Find Max Density :
        Color=max(Img.getcolors(Img.size[0]*Img.size[1]))
        Color=Color[1]

        #* Check With Threshold Limit :
        if(Color<=Brightness_Threshold):
            Result=True
        else:
            Result=False

        #* Remove Temp Image :
        os.remove("Result.jpg") 

    except Exception:
        raise HTTPException(status_code=500, detail='Something went wrong')
    
    return {"Success": f"Result :{Result} - Background Color(GrayScale): {Color}"}


if __name__ == "__main__":
     uvicorn.run("Main:app", host="0.0.0.0", port=8000,reload=True)