# downloader/views.py

from django.shortcuts import render, redirect
from .forms import YouTubeLinkForm
from pytube import YouTube
import threading
import os
from django.contrib import messages

def download_complete(request):
    # Especifica o caminho para "C:/Downloads"
    downloads_path = 'C:/Downloads'
    
    return render(request, "final.html", {'downloads_path': downloads_path})

def download_video_view(request):
    if request.method == 'POST':
        form = YouTubeLinkForm(request.POST)
        if form.is_valid():
            link = form.cleaned_data['link']
            yt = YouTube(link)
            
            try:
                # Getting the highest resolution
                yd = yt.streams.get_highest_resolution()
                
                # Function to download the video
                def download(): 
                    # Especifica o caminho para "C:/Downloads"
                    downloads_path = 'C:/Downloads'
                    
                    # Cria o diretório se não existir
                    if not os.path.exists(downloads_path):
                        os.makedirs(downloads_path)
                    
                    # Faz o download do vídeo
                    yd.download(output_path=downloads_path)
                    
                    # Adiciona uma mensagem de sucesso
                    messages.success(request, f"Download Concluído! Vídeo salvo em {downloads_path}")

                download_thread = threading.Thread(target=download)
                download_thread.start()

                return redirect('download_complete')

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

