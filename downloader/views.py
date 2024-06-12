# downloader/views.py

from django.shortcuts import render, redirect
from .forms import YouTubeLinkForm
from pytube import YouTube
import os
from django.http import StreamingHttpResponse
from django.contrib import messages
import tempfile

# Function to send the file as a streaming response
def file_iterator(file_name, chunk_size=8192):
    with open(file_name, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield chunk

def download_video_view(request):
    if request.method == 'POST':
        form = YouTubeLinkForm(request.POST)
        if form.is_valid():
            link = form.cleaned_data['link']
            yt = YouTube(link)

            try:
                # Getting the highest resolution
                yd = yt.streams.get_highest_resolution()

                # Define the temporary directory path
                temp_dir = tempfile.gettempdir()

                # Check if the directory exists, if not, create it
                if not os.path.exists(temp_dir):
                    os.makedirs(temp_dir)

                # Temporary file path
                temp_file_path = os.path.join(temp_dir, yd.default_filename)
                yd.download(output_path=temp_dir)

                response = StreamingHttpResponse(file_iterator(temp_file_path))
                response['Content-Type'] = 'video/mp4'
                response['Content-Disposition'] = f'attachment; filename="{yd.default_filename}"'

                # Optionally, you can remove the temporary file after sending it
                # os.remove(temp_file_path)

                return response

            except Exception as e:
                messages.error(request, f"Ocorreu um erro: {e}")
                return redirect('download_video')
    else:
        form = YouTubeLinkForm()

    return render(request, 'download.html', {'form': form})




# from django.shortcuts import render, redirect
# from .forms import YouTubeLinkForm
# from pytube import YouTube
# import threading
# import os
# from pathlib import Path
# from django.contrib import messages

# def download_complete(request):
#     # Determine the path to the Downloads directory
#     home = str(Path.home())
#     downloads_path = os.path.join(home, 'Downloads')
    
#     return render(request, "final.html", {'downloads_path': downloads_path})

# def download_video_view(request):
#     if request.method == 'POST':
#         form = YouTubeLinkForm(request.POST)
#         if form.is_valid():
#             link = form.cleaned_data['link']
#             yt = YouTube(link)
            
#             try:
#                 # Getting the highest resolution
#                 yd = yt.streams.get_highest_resolution()
                
#                 # Function to improve the download time
#                 def download(): 
#                     # Determine the path to the Downloads directory
#                     home = str(Path.home())
#                     downloads_path = os.path.join(home, 'Downloads')
#                     yd.download(output_path=downloads_path)
#                     messages.success(request, f"Download Concluído! Vídeo salvo em {downloads_path}")

#                 download_thread = threading.Thread(target=download)
#                 download_thread.start()

                
#                 return redirect('download_complete')

#             except Exception as e:
#                 messages.error(request, f"Ocorreu um erro: {e}")
#                 return redirect('download_video')
#     else:
#         form = YouTubeLinkForm()

#     return render(request, 'download.html', {'form': form})
