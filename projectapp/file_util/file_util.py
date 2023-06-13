### 파일 업로드(저장) 처리를 위한 라이브러리
from django.core.files.storage import FileSystemStorage

### 파일 다운로드 처리를 위한 라이브러리
from django.http import StreamingHttpResponse
from wsgiref.util import FileWrapper
import os
from django.http import HttpResponse



class File_Util :
    # - 파일 원본 정보
    file_nm = ""

    # - 파일 업로드 폴더 위치 지정
    upload_dir = ""
    
    # - 파일 다운로드 폴더 위치 지정
    img_dir = ""
    # - 이미지 등 페이지 static 경로 + 파일명
    img_full_name = ""
    
    # - 다운로드를 위한 전체경로 + 파일명
    download_dir = ""
    # - 다운로드를 위한 전체경로 + 파일명
    download_full_name = ""
    
    # - 파일 사이즈
    file_size = 0
    
    # - 순수 파일명
    filename = ""    
    
    
    #########################################    
    ############# [File Upload] ###########
    #########################################
    ### 업로드를 위해 멤버 변수 Setting
    def setUpload(self, file_nm, upload_dir, img_dir, download_dir) :
        self.file_nm    = file_nm
        self.upload_dir = upload_dir
        self.img_dir   = img_dir
        self.download_dir = download_dir
    
    ### 파일 업로드 함수
    def fileUpload(self) :
        ### 파일 처리를 위한 클래스 생성
        fs = FileSystemStorage(self.upload_dir, self.download_dir)
        
        ### 파일을 save_dir 폴더에 업로드(저장)하기
        ### - save(파일명, 파일정보) : 파일 업로드하기
        ### - self.filename : 실제 파일명
        self.filename = fs.save(self.file_nm.name, self.file_nm)
        
        ### 파일 업로드 이후 기본값 셋팅시키기
        self.setParameter(fs)
        
    ### 파일 업로드 이후 DB 또는 별도로 사용할 기본값 셋팅하기
    def setParameter(self, fs) :
        # - 파일사이즈
        self.file_size = self.file_nm.size
        
        # - 이미지 경로 : static 경로 + 파일명(경로 + 파일명) 
        self.img_full_name = self.img_dir + self.filename
        
        # - downlaod 경로 : download 경로 + 파일명(경로 + 파일명) 
        self.download_full_name = self.download_dir + self.filename
        