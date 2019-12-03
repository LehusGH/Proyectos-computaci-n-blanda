import { Component } from '@angular/core';
import {NavController} from '@ionic/angular';
import {SpeechRecognition} from '@ionic-native/speech-recognition/ngx';
import { matches } from '@ionic/core/dist/types/components/nav/view-controller';
import { match } from 'minimatch';

@Component({selector: 'app-home', templateUrl: 'home.page.html', styleUrls: ['home.page.scss'],})
export class HomePage
{
  msn: string = '';

  //Se consideraran 4 tipos de discuros: politicos, religiosos, empresariales.
  //El valor por defecto es de una charla casual
  politico:number = 0;
  fp:string[] = ['ustedes son el futuro del pais', 
                 'país', 'vamos a', 'el más educado', 'cuenten conmigo', 
                 'el voto es útil', 'cambiar', 'la política', 'corrupto', 'pueblo', 'paz'];
  canFp:number = this.fp.length;

  religioso:number = 0;
  fr:string[] = ['paz', 'creer', 'perdonar', 'ser', 'bueno', 'señor', 'dios', 'divinidad', 'divina', 
                 'misericordia', 'llorar', 'suplicas', 'cielo', 'paraiso', 'eternidad'];
  canFr:number = this.fp.length;

  empresarial:number = 0;
  fe:string[] = ['apreciados', 'tengo el', 'honor', 'departamento de', 'reporte', 'noticias', 
                 'crecimiento', 'proyectos', 'proyecciones', 'incrementar', 'supervisores', 
                 'empresa', 'equipo', 'esfuerzo', 'empleados'];
  canFe:number = this.fp.length;

  //Cambiamos el color del fondo de la aplicacion
  bgcolor: string = 'white';

  //Creamos el constructor de la clase
  constructor(public navCtrl: NavController, private sr: SpeechRecognition){}

  //Cuando se ejecuta la app por primera vez se pide el permiso de acceso al microfono
  ionViewDidLoad()
  {
    this.getPermission();
  }

  //Esta funcion se encarga de realizar el reconocimiento de voz
  startListening()
  {
    //Establecemos el lenguaje y la cantidad de variantes de una frase escuchada
    let options = {language: 'es-ES', matches: 1,}

    //Se guarda el mensaje escuchado en msn
    this.sr.startListening(options).subscribe(
      matches=>{this.msn = matches[0];}
    )
    this.generarTipo();
  }

  generarTipo()
  {
    //Revisa los elementos de la el arreglo de frases comunes en discursos politicos
    for(var e=0; e<this.canFp; e++)
    {
      if(this.msn.includes(this.fp[e]))
      {
        this.politico = this.politico + (100 / this.canFp);
      }
    }

    //Revisa los elementos de la el arreglo de frases comunes en discursos religiosos
    for(var e=0; e<this.canFr; e++)
    {
      if(this.msn.includes(this.fr[e]))
      {
        this.religioso = this.religioso + (100 / this.canFr);
      }
    }

    //Revisa los elementos de la el arreglo de frases comunes en discursos empresariales
    for(var e=0; e<this.canFe; e++)
    {
      console.log(this.empresarial);
      if(this.msn.includes(this.fe[e]))
      {
        this.empresarial = this.empresarial + (100 / this.canFe);
      }
    }

    //Se utiliza la convencion de que si el mayor numero logrado entre los 3 tipos de discurso es menos
    //al 30% de los matches, entonces es considerado una charla casual.
    //Si no es asi, se asigna una frase de salida dependiendo de el numero mayor
    if(this.empresarial > this.politico && this.empresarial > this.religioso && this.empresarial > 30)
    {
      this.msn = 'Este es un discurso empresarial';
    }
    else if(this.religioso > this.politico && this.empresarial < this.religioso && this.religioso > 30)
    {
      this.msn = 'Este es un discurso religioso';
    }
    else if(this.religioso < this.politico && this.politico > this.empresarial && this.politico > 30)
    {
      this.msn = 'Este es un discurso político';
    }
    else{
      this.msn = 'Este es una conversacion casual';
    }
  }

  //Se prueba si la aplicacion tiene permisos. Si los tiene no los vuelve a pedir
  getPermission()
  {
    this.sr.hasPermission().then((hasPermission:boolean)=>{
      if(!hasPermission)
      {
        this.sr.requestPermission();
      }
    })
  }
}