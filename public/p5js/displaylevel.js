class displaylevel {

  constructor(w) {
    this.b = height / 2;
    this.l = this.b - height / 4;
    this.lowl = this.b - height / 32;
    this.bw = w;
    this.w = w;
    this.c = [color(20,60, 220), color(220, 220, 60), color(220, 60, 60)];
    this.in = 0;
    this.lh1 = this.b;
    this.lh2 = this.b;
    this.cn1 = [width / 6, this.b];
    this.cn2 = [width - this.cn1[0], this.b];
    this.v1 = [width / 4.5, this.b];
    this.v5 = [width - this.v1[0], this.b];
    this.v2 = [width / 3, this.b];
    this.v4 = [width - this.v2[0], this.b];
    this.v3 = [width / 2, this.b];
  }

  display() {
    stroke(this.getColor(this.in));
    strokeWeight(this.w);
    noFill();
    beginShape();
    curveVertex(this.cn1[0], this.cn1[1]);
    curveVertex(this.v1[0], this.v1[1]);
    curveVertex(this.v2[0], this.lh2);
    curveVertex(this.v3[0], this.lh1);
    curveVertex(this.v4[0], this.lh2);
    curveVertex(this.v5[0], this.v5[1]);
    curveVertex(this.cn2[0], this.cn2[1]);
    endShape();
    beginShape();
    curveVertex(this.cn1[0], height - this.cn1[1]);
    curveVertex(this.v1[0], height - this.v1[1]);
    curveVertex(this.v2[0], height - this.lh2);
    curveVertex(this.v3[0], height - this.lh1);
    curveVertex(this.v4[0], height - this.lh2);
    curveVertex(this.v5[0], height - this.v5[1]);
    curveVertex(this.cn2[0], height - this.cn2[1]);
    endShape();
    this.drawLimit();
  }

  drawLimit() {
    stroke(this.c[2]);
    strokeWeight(this.bw);
    noFill();
    beginShape();
    curveVertex(this.cn1[0], this.cn1[1]);
    curveVertex(this.v1[0], this.v1[1]);
    curveVertex(this.v2[0], this.lowl);
    curveVertex(this.v3[0], this.l);
    curveVertex(this.v4[0], this.lowl);
    curveVertex(this.v5[0], this.v5[1]);
    curveVertex(this.cn2[0], this.cn2[1]);
    endShape();
    beginShape();
    curveVertex(this.cn1[0], height - this.cn1[1]);
    curveVertex(this.v1[0], height - this.v1[1]);
    curveVertex(this.v2[0], height - this.lowl);
    curveVertex(this.v3[0], height - this.l);
    curveVertex(this.v4[0], height - this.lowl);
    curveVertex(this.v5[0], height - this.v5[1]);
    curveVertex(this.cn2[0], height - this.cn2[1]);
    endShape();
  }

  update(l) {
    this.in = l;
    this.lh1 = map(this.in, 0, 1, this.b, this.l);
    this.lh2 = map(this.in, 0, 1, this.b, this.lowl);
  }

  getColor(l) {
    if (l < 0.1) {
      this.w = this.bw;
      return this.c[0];
    } else if (l >= 0.1 && l < 0.4) {
      this.w = this.bw + 2;
      return this.c[1];
    } else {
      this.w = this.bw + 5;
      return this.c[2];
    }
  }

}
