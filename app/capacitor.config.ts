import type { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'com.eday.app',
  appName: 'eday',
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
