import axios from 'axios'

type APIResponse = {
  pred: string;
}

const canvas = document.getElementById("canvas") as HTMLCanvasElement;
const ctx = canvas.getContext('2d') as CanvasRenderingContext2D;
const clearbutton = document.getElementById("clear") as HTMLButtonElement;
const savebutton = document.getElementById("save") as HTMLButtonElement;
const predictiontext = document.getElementById("prediction") as HTMLParagraphElement;

var isdown: boolean = false;
ctx.fillStyle = 'black';
const rect:DOMRect = canvas.getBoundingClientRect();
let lastpost = {x:0,
   y:0}


function ondown(e:MouseEvent) {
  isdown = true;
  lastpost["x"] = e.clientX - rect.left
  lastpost["y"] = e.clientY - rect.top
}

function onmove(e: MouseEvent) {
  if (isdown) {
    ctx.beginPath();
    ctx.lineWidth = 5
    ctx.moveTo(lastpost["x"],lastpost["y"])
    var posdict = {
      x: (e.clientX - rect.left),
      y: (e.clientY - rect.top)
    };
    lastpost["x"] = posdict["x"]
    lastpost["y"] = posdict["y"]
    ctx.lineTo(posdict["x"],posdict["y"])
    ctx.stroke()

  }
}

function onup() {
  isdown = false;
}

function clear() {
  ctx.clearRect(0,0,canvas.width,canvas.height);
}


function saveimg() {
  predictiontext.innerHTML = "";
  let imageb64: string = canvas.toDataURL("image/png");
  navigator.clipboard.writeText(imageb64);

  // Alert the copied text
  alert("Copied the text: ");
  let resp = (postimage(imageb64));
  resp.then(r => {
    if (typeof r === "string") {
      console.log("error");

    } else {
      let pred = r["pred"];
      predictiontext.innerHTML = "The image is the letter " + pred;
    }
  })

}

async function postimage(b64: string) {
  try {
    // 👇️ const data: CreateUserResponse
    const { data } = await axios.post<APIResponse>(
      'http://127.0.0.1:8000/predict',
      { image: b64 },
      {
        headers: {
          'Content-Type': 'application/json',
          Accept: 'application/json',
        },
      },
    );

    return data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      console.log('error message: ', error.message);
      return error.message;
    } else {
      console.log('unexpected error: ', error);
      return 'An unexpected error occurred';
    }
  }
}

canvas.addEventListener('mousedown', ondown);
canvas.addEventListener('mousemove', onmove);
canvas.addEventListener('mouseup', onup);
clearbutton.addEventListener('click', clear);
savebutton.addEventListener('click', saveimg);





