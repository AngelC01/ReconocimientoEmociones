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
            Aceptar.Clicked += Aceptar_Clicked;

        }

        private void Aceptar_Clicked(object sender, EventArgs e)
        {
            modal2.IsVisible = false;
        }

        private async void HacerPostAsync()
		{



            modal.IsVisible = true;
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
                modal.IsVisible = false;
                if (emociones.Errormsg.Equals("No se encontro ningun rostro"))
                {
                    modal2.IsVisible = true;
                    ImageEmocion.Source = "ErrorRostro";
                    EmocionModalLabel.Text = "Error: " + emociones.Errormsg;

                }
                //DisplayAlert("Error"," :( "+ emociones.Errormsg, "Aceptar");

			}
			else
			{


                ImageEmocion.Source = emociones.Emocion;
                EmocionModalLabel.Text = "Su emocion es: " + emociones.Emocion;
                modal.IsVisible = false;
                modal2.IsVisible = true;
               // Emocionlabel.Text = "Su emocionn es: " + emociones.Emocion;
                

            }

        }

		private void SubirArchivo_Clicked(object sender, EventArgs e)
		{
			if (Foto.Source == null)
			{
                DisplayAlert("Error", "Debe tomarse una foto", "Aceptar");

			}
			else
			{
                try
                {

                    HacerPostAsync();
                }catch(Exception g)
                {
                    DisplayAlert("Error", "Ocurrio un Error inesperado intentelo de nuevo", "Aceptar");


                }

            }
           
		}

     
    }
}
