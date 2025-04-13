import { CapacitorBarcodeScanner } from '@capacitor/barcode-scanner';
import { redeemEventSecret, setAdminToken, setUserId } from './handlers/index';

/* eslint-disable @typescript-eslint/no-explicit-any */
type tHandler<T = any> = {
	[key: string]: (...args: any[]) => T;
};

type tHandlerFunction = tHandler[keyof tHandler];

class QRCodeResponseHandler {
	public handlers = {} as tHandler;

	constructor() {}

	/**
	 * Inserts a handler
	 * @param prefix
	 * @param callback
	 */
	public insert(prefix: string, callback: tHandlerFunction) {
		this.handlers[prefix] = callback;
	}

	/**
	 * Runs the appropriate handler based on the response prefix.
	 * Removes the prefix before passing the remaining response.
	 * @param response - The response string to process.
	 */
	public run(response: string): void {
		// Iterate through registered handlers
		for (const prefix in this.handlers) {
			if (response.startsWith(prefix)) {
				// Handler Matched
				console.info(
					`[QRCodeResponseHandler] Handler found for response: ${response}. Matched Prefix: ${prefix}`
				);
				const trimmedResponse = response.slice(prefix.length);
				this.handlers[prefix](trimmedResponse);
				return;
			}
		}

		// No Matches
		console.warn(`[QRCodeResponseHandler] No handler found for response: ${response}`);
	}

	public async prompt() {
		const qr_response = await CapacitorBarcodeScanner.scanBarcode({
			hint: 0,
			cameraDirection: 1,
			scanOrientation: 1
		});

		this.run(qr_response.ScanResult);
	}
}

const qrCodeResponseHandler = new QRCodeResponseHandler();

qrCodeResponseHandler.insert('set-user-id:', setUserId);
qrCodeResponseHandler.insert('set-admin-token:', setAdminToken);
qrCodeResponseHandler.insert('redeem-event-secret:', redeemEventSecret)

export default qrCodeResponseHandler;
