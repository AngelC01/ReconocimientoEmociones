using Newtonsoft.Json;
using Plugin.Media;
using Plugin.Media.Abstractions;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using Xamarin.Forms;

namespace proyecto
{
	public partial class MainPage : ContentPage
	{
        private MediaFile _image;

        public MainPage()
		{
			InitializeComponent();
            takePhoto.Clicked += async (sender, args) =>
            {
                await CrossMedia.Current.Initialize();

                if (!CrossMedia.Current.IsCameraAvailable || !CrossMedia.Current.IsTakePhotoSupported)
                {
                    DisplayAlert("No Camera", ":( No camera available.", "OK");
                    return;
                }

                var file = await CrossMedia.Current.TakePhotoAsync(new Plugin.Media.Abstractions.StoreCameraMediaOptions
                {
                   // Directory = "Sample",
                   // Name = "test.jpg",
                    SaveToAlbum = true
                });

                if (file == null)
                    return;
                _image = file;
                //await DisplayAlert("File Location", file.Path, "OK");

                Foto.Source = ImageSource.FromStream(() =>
                {
                    var stream = file.GetStream();
                    return stream;
                });
            };

        }

      
        private async void HacerPostAsync()
		{
            
           
        // code here to assign image to _image
            var content = new MultipartFormDataContent();
            content.Add(new StreamContent(_image.GetStream()), "\"pic\"", $"\"album_camara\"");
            content.Add(new StreamContent(_image.GetStream()), "\"pic2\"", $"\"album_camara\"");

            var httpClient = new System.Net.Http.HttpClient();
            var url = "http://3c168f7042f6.ngrok.io/archivo";
            var url2 = urlTxt.Text;
            var responseMsg = await httpClient.PostAsync(url2, content);

            var remotePath = await responseMsg.Content.ReadAsStringAsync();

            Emociones emociones = new Emociones();
            emociones = JsonConvert.DeserializeObject<Emociones>(remotePath);
			if (emociones.Error)
			{

                DisplayAlert("Error"," :( "+ emociones.Errormsg, "Aceptar");

			}
			else
			{
                Emocionlabel.Text = "Su emocionn es: " + emociones.Emocion;


            }

        }

		private void SubirArchivo_Clicked(object sender, EventArgs e)
		{
			if (Foto.Source == null)
			{
                DisplayAlert("Error", "Debe tomarse una foto", "OK");

			}
			else
			{
                HacerPostAsync();
            }
           
		}
	}
}
