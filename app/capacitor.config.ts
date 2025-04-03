import type { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'com.eday.app',
  appName: 'AcePreneur',
  webDir: 'www',
  plugins: {
    "CapacitorBarCodeScanner": {
      "android": {
        "permissions": ["android.permission.CAMERA"]
      } 
    },
    CapacitorHttp: {
      enabled: true,
    }
  }
};

export default config;
