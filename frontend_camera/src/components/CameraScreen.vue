<template>
  <div class="camera-screen" ref="container">
    <div class="controls">
      <label for="camera" v-if="options.length > 1">
        <select
          @change="getCameraStream"
          v-model="selectedCamera"
          id="camera"
        >
          <option
            v-for="option in options"
            :key="option.id"
            :value="option.id"
          >
            {{option.text}}
          </option>
        </select>
      </label>
      <button type="button" class="btn submit" @click="startDetection">Start detection</button>
      <button type="button" class="btn" @click="$emit('goBack')">Back</button>
      <p>
        Detection status:
        <span v-if="shouldCheckCrossing">Running</span>
        <span v-else>Waiting</span>
      </p>
    </div>

    <div class="video-container">
      <canvas ref="canvas" />
      <video
        ref="video"
        loop
        muted
        type="video/mp4"
        autoplay="autoplay"
      />
      <!-- :src="`${publicPath}video_2022-06-15_12-11-10.mp4`" -->
      <DetectedFramesList :detected="detected" @deleteCrossing="deleteCrossing" />
    </div>

  </div>
</template>

<script>
import Cookies from 'js-cookie';
import DetectedFramesList from 'components/DetectedFramesList';


// cv is dummy. using node module will turn your pc into the toaster, so using a cdn;
// also, cv can't support reactive props, so here's a bunch of lets;
let { cv } = window.cv;
let frame = null;
let fgMask = null;
let bgSubstractor = null;
let cvVideoCapture = null;
let kernel = null;

const DEBOUNCE_TIME_MS = 10000;
const BG_SUBSTRACTOR_MEMORY = 100;
const BG_SUBSTRACTOR_THRESHOLD = 150;
const MIN_AREA = 3000;
const FPS = 60;


const getBoundingRectFromContour = contour => {
  if (cv.contourArea(contour) < MIN_AREA) {
    return null;
  }
  return cv.boundingRect(contour);
};


const checkCrossing = (rect, threshold) => {
  const { x, width } = rect;
  return x <= threshold || (x + width) >= threshold;
};


export default {
  components: {
    DetectedFramesList,
  },


  data: () => ({
    video: null,
    stream: null,
    selectedCamera: Cookies.get('camera'),
    timeout: null,
    publicPath: process.env.BASE_URL,
    detected: {},
    shouldCheckCrossing: false,
    options: [],
  }),


  methods: {

    destroy() {
      this.stopStream();
      this.stream = null;
      this.stopCvProcessing();
    },


    stopCvProcessing() {
      clearTimeout(this.timeout);
      if (frame) {
        frame.delete();
        frame = null;
      }
      if (fgMask) {
        fgMask.delete();
        fgMask = null;
      }
      if (bgSubstractor) {
        bgSubstractor.delete();
        bgSubstractor = null;
      }
    },


    stopStream() {
      if (this.stream) {
        this.stream.getTracks().forEach(track => {
          track.stop();
        });
      }
    },


    handleError(error) {
      console.error('error', error);
    },


    getCameraStream() {
      this.stopStream();
      Cookies.set('camera', this.selectedCamera);

      const constraints = {
        video: {
          deviceId: { exact: this.selectedCamera },
        },
      };
      navigator.mediaDevices
        .getUserMedia(constraints)
        .then(this.handleCameraStream)
        .catch(this.handleError);
    },


    handleCameraStream(stream) {
      this.stream = stream;
      this.$refs.video.srcObject = stream;
      this.$refs.video.play();
      this.stream.getTracks().forEach(track => {
        track.start();
      });
      this.initMotionDetection();
    },


    handleDevicesInfo(deviceInfos) {
      const options = [];
      deviceInfos.forEach(deviceInfo => {
        const option = {};
        option.id = deviceInfo.deviceId;

        if (deviceInfo.kind === 'videoinput') {
          if (!this.selectedCamera) {
            this.selectedCamera = option.id;
          }
          option.text = deviceInfo.label || `camera ${options.length + 1}`;
          options.push(option);
        }
      });
      this.options = options;
    },


    initVideoCapture() {
      navigator.mediaDevices
        .enumerateDevices()
        .then(this.handleDevicesInfo)
        .then(this.getCameraStream)
        .catch(this.handleError);
    },


    initMotionDetection() {
      if (!cv) {
        return;
      }
      this.stopCvProcessing();

      const WIDTH = 200;
      const HEIGHT = Math.round((this.$refs.video.videoHeight / this.$refs.video.videoWidth) * WIDTH);
      this.$refs.video.width = WIDTH;
      this.$refs.video.height = HEIGHT;
      this.$refs.canvas.width = WIDTH;
      this.$refs.canvas.height = HEIGHT;

      cvVideoCapture = new cv.VideoCapture(this.$refs.video);
      frame = new cv.Mat(HEIGHT, WIDTH, cv.CV_8UC4);
      fgMask = new cv.Mat(HEIGHT, WIDTH, cv.CV_8U);
      kernel = cv.Mat.ones(5, 5, cv.CV_8U);
      bgSubstractor = new cv.BackgroundSubtractorMOG2(BG_SUBSTRACTOR_MEMORY, BG_SUBSTRACTOR_THRESHOLD, true);

      this.timeout = setTimeout(this.processFrame, 0);
    },


    processFrame() {
      try {
        if (!cvVideoCapture) {
          return;
        }
        const begin = Date.now();
        cvVideoCapture.read(frame);
        bgSubstractor.apply(frame, fgMask);
        // de-noise
        cv.morphologyEx(fgMask, fgMask, cv.MORPH_CLOSE, kernel, new cv.Point(-1, -1), 2);
        const contours = new cv.MatVector();
        cv.findContours(fgMask, contours, new cv.Mat(), cv.RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE);

        for (let i = 0; i < contours.size(); i += 1) {
          const rect = getBoundingRectFromContour(contours.get(i));
          if (rect) {
            this.processDetection(rect);
          }
        }

        this.drawDetectionLine();
        cv.imshow(this.$refs.canvas, frame);
        const delay = 1000 / FPS - (Date.now() - begin);
        clearTimeout(this.timeout);
        this.timeout = setTimeout(this.processFrame, delay);
      }
      catch (e) {
        console.error('error', e);
        this.stopCvProcessing();
      }
    },


    async debounceCrossingCheck() {
      this.shouldCheckCrossing = false;
      await setTimeout(() => {
        this.shouldCheckCrossing = true;
      }, DEBOUNCE_TIME_MS);
    },


    processDetection(rect) {
      const { width } = this.$refs.video;
      const point1 = new cv.Point(rect.x, rect.y);
      const point2 = new cv.Point(rect.x + rect.width, rect.y + rect.height);
      const isCrossing = checkCrossing(rect, width / 2);
      if (isCrossing && this.shouldCheckCrossing) {
        const time = new Date();
        const id = time - 0;
        const crossingFrame = new ImageData(new Uint8ClampedArray(frame.data), frame.cols, frame.rows);
        this.detected[id] = {
          time,
          crossingFrame,
        };
        this.debounceCrossingCheck();
      }
      cv.rectangle(frame, point1, point2, [255, 0, 255, 255], 2, cv.LINE_AA, 0);
    },


    drawDetectionLine() {
      const { width, height } = this.$refs.video;
      const point1 = new cv.Point(width / 2, 0);
      const point2 = new cv.Point(width / 2, height);
      cv.line(frame, point1, point2, [255, 0, 0, 255], 2, cv.LINE_AA, 0);
    },


    cvIsReady() {
      return new Promise(resolve => {
        const check = () => {
          this.timeout = setTimeout(() => {
            if (window.cv && this.stream) {
              cv = window.cv;
              resolve();
              return;
            }

            check();
          }, 500);
        };

        check();
      });
    },


    deleteCrossing(id) {
      delete this.detected[id];
    },


    startDetection() {
      this.shouldCheckCrossing = true;
      document.scrollingElement.scrollTo(0, 1000);
    },

  },


  mounted() {
    this.initVideoCapture();
    this.cvIsReady().then(this.initMotionDetection);
  },


  beforeUnmount() {
    this.destroy();
  },
};
</script>

<style lang="scss" scoped>
.video-container,
.camera-screen {
  display: flex;
  flex-direction: column;
  position: relative;
  width: 100%;

  video {
    // opacity: 0;
    height: 100vh;
    width: auto;
    position: absolute;
    left: 0;
    right: 0;
    opacity: 0;
  }

  canvas {
    max-height: 100vh;
  }

  .video-container {
    background-color: black;
  }

  .controls {
    display: flex;
    flex-direction: column;
    z-index: 200;
  }
}
</style>
