
import functools


class GetSHA1Hash:
    def __init__(self, data):
        self.data = data
        self.h = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0]

    
    def preprocessing(self):
        preprocessed=[bin(ord(x))[2:].rjust(8, '0') for x in self.data]
        preprocessed="".join(preprocessed)
        preprocessed+='1'
        return preprocessed

    def padding(self):
        padded_data = self.preprocessed
        while(len(padded_data)%512 != 448):
            padded_data+='0'        
        return padded_data

    @staticmethod
    def pad(str, bits):
        res = str
        while (len(res)%bits!=0):
            res = '0' + res
        return res

    @staticmethod
    def split_chunks(chunk, size):
        return [
            chunk[i : i + size] for i in range(0, len(chunk), size)
        ]
    
    @staticmethod
    def rotate(bits, turns):       
        return bits[turns:]+bits[0:turns]

    def uppendLenght(self):
        len_data = len(self.preprocessed)-1
        binaryLen = bin(len_data)[2:].rjust(64,'0')
        prepared=self.padded_data+binaryLen
        return prepared

    

    def hashing(self):
        self.preprocessed= self.preprocessing()
        self.padded_data= self.padding()
        self.prepared = self.uppendLenght()
        self.chunks = self.split_chunks(self.prepared,512)
       
        for chunk in self.chunks:
            smallChunks = self.split_chunks(chunk,32)
            
            for i in range(16, 80):
                
                # wordA=smallChunks[i - 3]
                # wordB=smallChunks[i - 8]
                # wordC=smallChunks[i - 14]
                # wordD=smallChunks[i - 16]
                # xorA=int(wordA,2)^int(wordB,2)
                # xorB=xorA^int(wordC,2)
                # xorC=xorB^int(wordD,2)

                # binar = str(bin(xorC))[2:]
                # paddedBin = self.pad(binar,32)
                # word = self.rotate(paddedBin,5)
                # smallChunks.append(word)
                val = functools.reduce(lambda acc, curr: acc^curr,map(lambda e:int(e,2),[smallChunks[i - 3], smallChunks[i - 8], smallChunks[i - 14], smallChunks[i - 16]]))
                binar = str(bin(val>>0))[2:]
                paddedBin = self.pad(binar,32)
                word = self.rotate(paddedBin,1)
                smallChunks.append(word)

            a, b, c, d, e = self.h
        

            for i in range(0, 80):
                if 0 <= i < 20:
                    f = (b & c) | ((~b) & d)
                    k = 0x5A827999
                elif 20 <= i < 40:
                    f = b ^ c ^ d
                    k = 0x6ED9EBA1
                elif 40 <= i < 60:
                    f = (b & c) | (b & d) | (c & d)
                    k = 0x8F1BBCDC
                elif 60 <= i < 80:
                    f = b ^ c ^ d
                    k = 0xCA62C1D6

                ##f>>=0

                aRot=self.rotate(self.pad(str(bin(a))[2:],32),5)
                aInt =int(aRot,2)
                wordInt = int(smallChunks[i],2)
                t= aInt + f + e + k + wordInt & 0xFFFFFFFF
                e=d
                d=c
                bRot = self.rotate(self.pad(str(bin(b))[2:],32),30)
                c=int(bRot,2)
                b=a
                a=t
                #print(f"t={i}\t{hex(a)[2:].rjust(8,'0')}\t{hex(b)[2:].rjust(8,'0')}\t{hex(c)[2:].rjust(8,'0')}\t{hex(d)[2:].rjust(8,'0')}\t{hex(e)[2:].rjust(8,'0')}")



            self.h = (
            self.h[0] + a & 0xFFFFFFFF,
            self.h[1] + b & 0xFFFFFFFF,
            self.h[2] + c & 0xFFFFFFFF,
            self.h[3] + d & 0xFFFFFFFF,
            self.h[4] + e & 0xFFFFFFFF,
            )
        return "%08x %08x %08x %08x %08x" % tuple(self.h)


def main():
    hash_input = 'abc'
    print(f"Input value: {hash_input}")
    print(f"Result: {GetSHA1Hash(hash_input).hashing()}") #Result: a9993e36 4706816a ba3e2571 7850c26c 9cd0d89d
    hash_input = 'abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq'
    print(f"Input value: {hash_input}")
    print(f"Result: {GetSHA1Hash(hash_input).hashing()}") #Result: 84983e44 1c3bd26e baae4aa1 f95129e5 e54670f1
    # hash_input = 'a'*1000000
    # print(f"Input value: {hash_input}")
    # print(f"Result: {GetSHA1Hash(hash_input).hashing()}") #Result: 34aa973c d4c4daa4 f61eeb2b dbad2731 6534016f
    

 
 
if __name__ == "__main__":
    main()
