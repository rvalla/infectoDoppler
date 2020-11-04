class dopplerAudio {

  constructor(sf, mf) {
    this.d = 0;
    this.df = 1;
    this.p1 = createVector(0, 0);
    this.p2 = createVector(0, 0);
    this.isPlaying = false;
    this.state = 0;
    this.sf = sf;
    this.mf = mf;
    this.sin = new p5.SinOsc();
    this.mns = new p5.SqrOsc();
    this.ns = new p5.Noise("brown");
    this.sin.freq(sf);
    this.mns.freq(mf);
    this.mns.disconnect();
    this.sin.amp(0.6);
    this.mns.amp(0.5);
    this.ns.amp(this.mns);
  }

  play() {
    if (this.isPlaying === false) {
      switch (this.state) {
        case 0:
          this.sin.start();
          this.isPlaying = true;
          break;
        case 1:
          this.ns.start();
          this.mns.start();
          this.isPlaying = true;
          break;
        default:
          break;
      }
    }
  }

  stop() {
    if (this.isPlaying === true) {
      switch (this.state) {
        case 0:
          this.sin.stop();
          this.isPlaying = false;
          this.state = 1;
          break;
        case 1:
          this.ns.stop();
          this.mns.stop();
          this.isPlaying = false;
          this.state = 0;
          break;
        default:
          break;
      }
    }
  }

  updateDopplerFactor(p1, p2) {
    let newd = p5.Vector.mag(p5.Vector.sub(p1, p2));
    let s = constrain(this.d - newd, -25, 25);
    this.df = map(s, -25, 25, 0, 2);
    this.d = newd;
  }

  updateOscillator() {
    switch (this.state) {
      case 0:
        this.updateSin();
        break;
      case 1:
        this.updateNs();
        break;
    }
  }

  updateSin() {
    this.sin.freq(this.sf * this.df);
  }

  updateNs() {
    this.mns.freq(this.mf * this.df);
  }

}
