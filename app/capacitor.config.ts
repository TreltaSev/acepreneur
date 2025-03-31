import type { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'com.dt-acepreneur.app',
  appName: 'acepreneur',
  webDir: 'www',
  plugins: {
    "CapacitorBarCodeScanner": {
      "android": {
        "permissions": ["android.permission.CAMERA"]
      } 
    }
  }
};

export default config;
