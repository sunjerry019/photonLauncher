#include <iostream>
#include <libusb.h>
using namespace std;

void printdev(libusb_device *dev);

int main(){
	libusb_device **devs;
	libusb_context *ctx = NULL;
	int r;
	ssize_t cnt;
	
	r = libusb_init(&ctx);
	if(r < 0){
		cout << "Init error." << r <<endl;
		return 1;
	};
	libusb_set_debug(ctx, 3)
	cnt = libusb_get_device_list(ctx, &devs);
	
	if (cnt < 0){
		cout << "Get device error " << cnt << endl;
	};
	ssize_t i;
	for (i = 0; i < cnt; i++){
		printdev(devs[i])
	};
	libusb_free_device_list(devs, 1); 
	libusb_exit(ctx); 
	return 0;

}
