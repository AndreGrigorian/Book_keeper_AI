//
//  ContentView.swift
//  secondapp
//
//  Created by Andre Grigorian on 8/18/22.
//

import SwiftUI

struct ContentView: View {
    var body: some View {
        ZStack{
            BackgroundView(topColor: .black, bottomColor: .blue)
            VStack{
                //title textbox submit codeImage
                AppTitle(text: "QR Code Linker")
                URLForm()
                
                Image("qrcode")
                    .resizable()
                    .frame(width: 200, height: 200)
                    .padding(.vertical, 50)
                
                ScanStatus()

                

            }.padding(.bottom, 30)
            
        }
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
            .previewInterfaceOrientation(.portrait)
            
            
    }
}

struct BackgroundView: View{
    var topColor: Color
    var bottomColor: Color
    
    var body: some View{

        LinearGradient(colors: [topColor,bottomColor], startPoint: .topLeading,
            endPoint: .bottomTrailing)
        .edgesIgnoringSafeArea(.all)
    }
}

struct AppTitle:View{
    var text: String
    var body: some View{
        Text(text)
            .font(.system(size:32,
                          weight:.bold,
                          design: .default))
            .foregroundColor(.blue)
            .padding(.top,30)
    }
}

struct URLForm: View{
    @State private var url: String = ""
    var body: some View{
        HStack(alignment: .center){ //textbox, take to link
            TextField("Enter URL", text: $url)
                .padding()
                .background(.white)
                .foregroundColor(Color.black)
                .font(.system(size:20,
                              design: .default))
                .cornerRadius(5)
                .padding()
                            
            Button(action:{
                //do something
                if let link = URL(string: url) {
                  UIApplication.shared.open(link)
                }
//                print("\(url)")
            }, label: {
                Image(systemName:"arrowshape.turn.up.right.fill").renderingMode(.original)
                    .resizable()
                    .aspectRatio(contentMode: .fit)
                    .frame(width: 25, height: 25)
                    .foregroundColor(Color.white)
            })
        }
        .padding(.vertical, 40)
        .padding(.horizontal, 30)
//        .padding(.trailing, 30)
//        .padding(.leading, 20)
        
        Button{
            print("changed")
        }label: {
            Text("Change")
                .frame(width: 200, height: 50)
//                        .foregroundColor(.black)
                .background(Color.white)
                .font(.system(size: 25,weight: .bold,design: .default))
                .cornerRadius(10)
            
        }
    }
}

struct ScanStatus: View{
    var body: some View{
       
        Text("Scans:").font(.system(size:32,
                                   weight: .medium,
                                   design: .default))
                    .foregroundColor(.white)
        Text("67")
            .font(.system(size:32,
                        weight: .bold,
                        design: .default))
            .foregroundColor(.white)

    }
}
