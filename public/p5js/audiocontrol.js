class audiocontrol {

  constructor(amp) {
    this.a = amp;
    this.comp = new p5.Compressor();
    this.rev = new p5.Reverb();
    this.comp.set(0.005, 30, 12, -12, 0.5);
    this.rev.drywet(0.3);
    this.sf = new p5.SoundFile();
    this.mic = new p5.AudioIn();
    this.mic.start();
    this.mic.amp(this.a);
    this.rev.connect(this.mic);
    this.comp.connect(this.mic);
    this.rec = new p5.SoundRecorder();
    this.rec.setInput(this.mic);
    this.displayInput = new displaylevel(3);
  }

  record() {
    this.rec.record(this.sf);
  }

  stop() {
    this.rec.stop();
  }

  save() {
    saveSound(this.sf, "infectoDoppler.wav");
  }

  play() {
    this.sf.play();
  }

  display() {
    let level = this.mic.getLevel();
    this.displayInput.update(level);
    this.displayInput.display();
  }

  increaseInputLevel() {
    let l = constrain(this.a + 0.1, 0.0, 1.0);
    this.a = l;
    this.mic.amp(this.a);
  }

  decreaseInputLevel() {
    let l = constrain(this.a - 0.1, 0.0, 1.0);
    this.a = l;
    this.mic.amp(this.a);
  }

}
