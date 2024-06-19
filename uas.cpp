#include<iostream>
#include<time.h>
using namespace std;
void kuitansi(int diskon, int belanja, int jumlah, int total);

int main(){
    int pilihan, jumlah, total, diskon, belanja;
    time_t now = time (0);
    char* dt = ctime(&now);
    
    cout<<"=======================================================\n";
    cout<<"                 TOKO SEMBAKO BERKAH                   \n";
    cout<<"          Jl. Ketintang Madya No.7 Surabaya            \n";
    cout<<"                 Telp.(021)789500132                   \n";
    cout<<"Credit by : Fachry Furqon."<<"                 "<< dt;
    cout<<"=======================================================\n";
    string produk[10] = {"Beras","Gula","Minyak Goreng","Telur"};
	cout<<"Berikut daftar barang yang kami jual"<<endl;
		for (int i=0; i<4; i++) {
		cout<<i+1<<". "<<produk[i]<<" \n";
	}
	cout<<"Masukan pilihan barang yang anda ingin beli (format 1 - 4) : ";
	cin>>pilihan;
	switch (pilihan){
		case 1 :
			cout<<"------------------------------------------\n";
			cout<<"Anda akan membeli beras"<<endl;
			cout<<"masukan jumlah barang yang ingin dibeli : ";
			cin>>jumlah;
			total = 6500 * jumlah;
			cout<<"------------------------------------------\n";
			cout<<"Total pembelian anda adalah Rp."<<total<<endl;
			cout<<"Total keuntungan toko adalah Rp."<<30 * total/100<<endl;
			break;
		case 2 :
			cout<<"------------------------------------------\n";
			cout<<"Anda akan membeli gula"<<endl;
			cout<<"Masukan jumlah barang yang ingin dibeli : ";
			cin>>jumlah;
			total = 5500 * jumlah;
			cout<<"------------------------------------------\n";
			cout<<"Total pembelian anda adalah Rp."<<total<<endl;
			cout<<"Total keuntungan toko adalah Rp."<<30 * total/100<<endl;
			break;
		case 3 :
			cout<<"------------------------------------------\n";
			cout<<"Anda akan membeli minyak gorang"<<endl;
			cout<<"Masukan jumlah barang yang ingin dibeli : ";
			cin>>jumlah;
			total = 12000 * jumlah;
			cout<<"------------------------------------------\n";
			cout<<"Total pembelian anda adalah Rp."<<total<<endl;
			cout<<"Total keuntungan toko adalah Rp."<<30 * total/100<<endl;
			break;
		case 4 :
			cout<<"------------------------------------------\n";
			cout<<"Anda akan membeli telur"<<endl;
			cout<<"Masukan jumlah barang yang ingin dibeli : ";
			cin>>jumlah;
			total = 8000 * jumlah;
			cout<<"------------------------------------------\n";
			cout<<"Total pembelian anda adalah Rp."<<total<<endl;
			cout<<"Total keuntungan toko adalah Rp."<<30 * total/100<<endl;
			break;
		default:
			cout<<"Salah Masukan Operator"<<endl;
			exit(0);
	}
	cout<<"=========================================="<<endl;
	if(jumlah>=5){
		diskon = 0.5 * total;
		cout<<"Anda mendapatkan diskon sebesar Rp. "<<diskon<<endl;
		belanja = total - diskon;
		cout<<"Total belanja anda adalah Rp. "<<belanja<<endl;
	}else{
		cout<<"Total belanja anda adalah Rp. "<<total<<endl;
	}
	cout<<endl;
	kuitansi(diskon, belanja, jumlah, total);
	cout<<endl;
	cout<<"=======================================================\n";
	cout<<"            TERIMA KASIH TELAH BERBELANJA              \n";
	cout<<"=======================================================\n";
	
	return 0;
}
void kuitansi(int diskon, int belanja, int jumlah, int total){
	if(jumlah>=5){
		cout<<"=======================================================\n";
		cout<<"                 KUITANSI PEMBAYARAN                   \n";
		cout<<"=======================================================\n";
		cout<<"Hasil diskon Rp. "<<diskon<<endl;
		cout<<"Hasil total belanja Rp. "<<belanja<<endl;	
	}else{
		cout<<"=======================================================\n";
		cout<<"                 KUITANSI PEMBAYARAN                   \n";
		cout<<"=======================================================\n";
		cout<<"TIdak mendapat diskon"<<endl;
		cout<<"Hasil total belanja Rp. "<<total<<endl;	
	}
}
