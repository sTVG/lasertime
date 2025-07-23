const canvas = document.getElementById('game');
const ctx = canvas.getContext('2d');
let width = canvas.width;
let height = canvas.height;
let score = 0;
let planets = [];
let astronaut = {x: width/2, y: height/2, r: 5, angle:0, orbit:60, speed:0.02};
let targetIndex = 0;
let orbits = 0;
let dev = document.getElementById('dev');

function rand(min,max){ return Math.random()*(max-min)+min; }

function addPlanet(){
  const size = rand(10,30);
  const x = rand(size, width-size);
  const y = rand(size, height-size);
  planets.push({x,y,size});
}

for(let i=0;i<3;i++) addPlanet();

function draw(){
  ctx.clearRect(0,0,width,height);
  ctx.fillStyle='#fff';
  planets.forEach((p,i)=>{
    ctx.beginPath();
    ctx.arc(p.x,p.y,p.size,0,Math.PI*2);
    ctx.fillStyle = i===targetIndex ? '#0f0':'#888';
    ctx.fill();
  });
  // draw astronaut
  let target = planets[targetIndex];
  let ax = target.x + Math.cos(astronaut.angle)*astronaut.orbit;
  let ay = target.y + Math.sin(astronaut.angle)*astronaut.orbit;
  ctx.beginPath();
  ctx.arc(ax, ay, astronaut.r,0,Math.PI*2);
  ctx.fillStyle='#fff';
  ctx.fill();
  astronaut.x=ax; astronaut.y=ay;
  astronaut.angle+=astronaut.speed;
  if(astronaut.angle>Math.PI*2){ astronaut.angle-=Math.PI*2; orbits++; }
  dev.textContent = `orbits:${orbits} orbitDist:${astronaut.orbit.toFixed(1)}`;
}

function nextPlanet(){
  score += Math.floor((planets[targetIndex].size/10));
  document.getElementById('score').textContent = score;
  targetIndex++;
  orbits=0;
  if(targetIndex>=planets.length){ addPlanet(); }
  astronaut.orbit = planets[targetIndex].size+30;
}

canvas.addEventListener('touchstart', () => {
  if(orbits===0){ score*=1.2; }
  if(orbits<5){
    nextPlanet();
  } else {
    alert('Crash!');
    reset();
  }
});

function reset(){
  if(score>0) saveScore(score);
  score=0; targetIndex=0; orbits=0; planets=[]; for(let i=0;i<3;i++) addPlanet();
}

function gameLoop(){ draw(); requestAnimationFrame(gameLoop); }

gameLoop();

if('serviceWorker' in navigator){ navigator.serviceWorker.register('service-worker.js'); }


function loadScores(){
  return JSON.parse(localStorage.getItem('scores')||'[]');
}
function saveScore(sc){
  const list = loadScores();
  list.push(sc);
  list.sort((a,b)=>b-a);
  localStorage.setItem('scores', JSON.stringify(list.slice(0,10)));
  renderLeaderboard();
}
function renderLeaderboard(){
  const div = document.getElementById('leaderboard');
  const list = loadScores();
  div.innerHTML = '<h3>Top 10</h3>' + list.map(s=>'<div>'+s+'</div>').join('');
}
renderLeaderboard();
