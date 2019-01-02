package main

import "C"

import (
	"encoding/binary"
	"encoding/hex"
	"fmt"
	"io/ioutil"
	"log"
	"strconv"
	"strings"
)

type uleb128 int32
type sleb128 int32

type dextypeitem struct {
	typeindex    uint16
	typedataitem dextypedataitem
}

type dextypelist struct {
	size uint32
	list []dextypeitem
}

type dexstringitem struct {
	stringdataoffset uint32
	size             uleb128
	value            string
}

type dextypedataitem struct {
	descriptoridx uint32
	data          dexstringitem
}

type dexprotodataitem struct {
	shortyidx          uint32
	returntypeidx      uint32
	parametersoffset   uint32
	shorty             dexstringitem
	returntype         dextypedataitem
	parameterstypelist dextypelist
}

type dexfielddataitem struct {
	classindex    uint16
	typeindex     uint16
	nameindex     uint32
	classitemdata dextypedataitem
	typeitemdata  dextypedataitem
	nameitemdata  dexstringitem
}

type dexmethoddataitem struct {
	classindex    uint16
	protoindex    uint16
	nameindex     uint32
	classitemdata dextypedataitem
	protoitemdata dexprotodataitem
	nameitemdata  dexstringitem
}

type encodedfield struct {
	fieldindex uleb128
	accessflag uleb128
	fielditem  dexfielddataitem
}

type encodedmethod struct {
	methodindex uleb128
	accessflag  uleb128
	codeoffset  uleb128
	methoditem  dexmethoddataitem
}

type dexclassdataobject struct {
	staticfieldsize   uleb128
	instancefieldsize uleb128
	directmethodsize  uleb128
	virtualmethodsize uleb128
	staticfields      []encodedfield
	instancefields    []encodedfield
	directmethods     []encodedmethod
	virtualmethods    []encodedmethod
}

type dexclassdataitem struct {
	classindex        uint32
	accessflag        uint32
	superclassindex   uint32
	interfaceoffset   uint32
	sourcefileindex   uint32
	annotationoffset  uint32
	classdataoffset   uint32
	staticvalueoffset uint32
	classdataitem     dexclassdataobject
	classitem         dextypedataitem
	superclassitem    dextypedataitem
}

type dexheader struct {
	magic           []byte
	version         int64
	checksum        uint32
	signature       string
	filesize        uint32
	headersize      uint32
	endiantag       uint32
	linksize        uint32
	linkoffset      uint32
	mapoffset       uint32
	stringidssize   uint32
	stringidsoffset uint32
	typeidssize     uint32
	typeidsoffset   uint32
	protoidssize    uint32
	protoidsoffset  uint32
	fieldidssize    uint32
	fieldidsoffset  uint32
	methodidssize   uint32
	methodidsoffset uint32
	classdefsize    uint32
	classdefoffset  uint32
	datasize        uint32
	dataoffset      uint32
}

type dex struct {
	bytes       []byte
	header      dexheader
	stringtable []dexstringitem
	typetable   []dextypedataitem
	prototable  []dexprotodataitem
	fieldtable  []dexfielddataitem
	methodtable []dexmethoddataitem
	classtable  []dexclassdataitem
	pointer     uint32
}

func (d *dex) new(path string) []string {
	b, err := ioutil.ReadFile(path)
	if err != nil {
		log.Fatal(err)
	}
	d.bytes = b
	return d.parse()
}

func (d *dex) readbytes(size uint32) []byte {
	data := d.bytes[d.pointer : d.pointer+size]
	d.pointer += size
	return data
}

func (d *dex) readuint16() uint16 {
	data := d.bytes[d.pointer : d.pointer+2]
	d.pointer += 2
	return binary.LittleEndian.Uint16(data)
}

func (d *dex) readuint32() uint32 {
	data := d.bytes[d.pointer : d.pointer+4]
	d.pointer += 4
	return binary.LittleEndian.Uint32(data)
}

func (d *dex) readuleb128() uint32 {
	var result uint32
	var ctr uint
	var cur byte = 0x80
	for (cur&0x80 == 0x80) && ctr < 5 {
		cur = d.bytes[d.pointer]
		result += uint32((cur & 0x7f)) << (ctr * 7)
		ctr++
		d.pointer++
	}
	return result
}

func (d *dex) readsleb128() int32 {
	var result int32
	var ctr uint
	var cur byte = 0x80
	var signBits int32 = -1
	for (cur&0x80 == 0x80) && ctr < 5 {
		cur = d.bytes[d.pointer]
		result += int32((cur & 0x7f)) << (ctr * 7)
		signBits <<= 7
		ctr++
		d.pointer++
	}
	if ((signBits >> 1) & result) != 0 {
		result += signBits
	}
	return result
}

func (d *dex) parsestringitem(offset uint32) {
	backuppointer := d.pointer
	d.pointer = offset
	size := d.readuleb128()
	data := dexstringitem{
		stringdataoffset: offset,
		value:            string(d.bytes[d.pointer : d.pointer+size]),
		size:             uleb128(size),
	}
	d.stringtable = append(d.stringtable, data)
	d.pointer += size
	d.pointer = backuppointer
}

func (d *dex) parsestring(start uint32, size uint32) {
	backuppointer := d.pointer
	d.pointer = start
	for element := uint32(0); element < size; {
		element++
		d.parsestringitem(d.readuint32())
	}
	d.pointer = backuppointer
}

func (d *dex) parsetypeitem(index uint32) {
	data := dextypedataitem{
		descriptoridx: index,
		data:          d.stringtable[index],
	}
	d.typetable = append(d.typetable, data)
}

func (d *dex) parsetype(start uint32, size uint32) {
	backuppointer := d.pointer
	d.pointer = start
	for element := uint32(0); element < size; {
		element++
		d.parsetypeitem(d.readuint32())
	}
	d.pointer = backuppointer
}

func (d *dex) parseprototypelist(start uint32) dextypelist {
	backuppointer := d.pointer
	d.pointer = start
	data := dextypelist{}
	data.size = d.readuint32()
	for element := uint32(0); element < data.size; element++ {
		typeindex := d.readuint16()
		typeitemdata := d.typetable[typeindex]
		data.list = append(data.list, dextypeitem{typeindex: typeindex, typedataitem: typeitemdata})
	}
	d.pointer = backuppointer
	return data
}

func (d *dex) parseproto(start uint32, size uint32) {
	backuppointer := d.pointer
	d.pointer = start
	for element := uint32(0); element < size; {
		element++
		shortyidx := d.readuint32()
		returntypeidx := d.readuint32()
		parametersoffset := d.readuint32()
		shorty := d.stringtable[shortyidx]
		returntype := d.typetable[returntypeidx]
		parameters := dextypelist{}
		if parametersoffset > 0 {
			parameters = d.parseprototypelist(parametersoffset)
		}
		data := dexprotodataitem{
			shortyidx:          shortyidx,
			returntypeidx:      returntypeidx,
			parametersoffset:   parametersoffset,
			shorty:             shorty,
			returntype:         returntype,
			parameterstypelist: parameters,
		}
		d.prototable = append(d.prototable, data)
	}
	d.pointer = backuppointer
}

func (d *dex) parsefield(start uint32, size uint32) {
	backuppointer := d.pointer
	d.pointer = start
	for element := uint32(0); element < size; {
		element++
		classindex := d.readuint16()
		typeindex := d.readuint16()
		nameindex := d.readuint32()
		classitem := d.typetable[classindex]
		typeitem := d.typetable[typeindex]
		nameitem := d.stringtable[nameindex]

		data := dexfielddataitem{
			classindex:    classindex,
			typeindex:     typeindex,
			nameindex:     nameindex,
			classitemdata: classitem,
			typeitemdata:  typeitem,
			nameitemdata:  nameitem,
		}
		d.fieldtable = append(d.fieldtable, data)
	}
	d.pointer = backuppointer
}

func (d *dex) parsemethod(start uint32, size uint32) {
	backuppointer := d.pointer
	d.pointer = start
	for element := uint32(0); element < size; {
		element++
		classindex := d.readuint16()
		protoindex := d.readuint16()
		nameindex := d.readuint32()
		classitem := d.typetable[classindex]
		protoitem := d.prototable[protoindex]
		nameitem := d.stringtable[nameindex]

		data := dexmethoddataitem{
			classindex:    classindex,
			protoindex:    protoindex,
			nameindex:     nameindex,
			classitemdata: classitem,
			protoitemdata: protoitem,
			nameitemdata:  nameitem,
		}
		d.methodtable = append(d.methodtable, data)
	}
	d.pointer = backuppointer
}

func (d *dex) parseencodedfield(size uint32) []encodedfield {
	var fields []encodedfield
	for element := uint32(0); element < size; element++ {
		fieldindex := d.readuleb128()
		accessflag := d.readuleb128()
		data := encodedfield{
			fieldindex: uleb128(fieldindex),
			accessflag: uleb128(accessflag),
			fielditem:  d.fieldtable[fieldindex],
		}
		fields = append(fields, data)
	}
	return fields
}

func (d *dex) parseencodedmethod(size uint32) []encodedmethod {
	var methods []encodedmethod
	for element := uint32(0); element < size; element++ {
		methodindex := d.readuleb128()
		accessflag := d.readuleb128()
		codeoffset := d.readuleb128()
		methoditem := d.methodtable[methodindex]
		data := encodedmethod{
			methodindex: uleb128(methodindex),
			accessflag:  uleb128(accessflag),
			codeoffset:  uleb128(codeoffset),
			methoditem:  methoditem,
		}
		methods = append(methods, data)
	}
	return methods
}

func (d *dex) parseclassdataitem(start uint32) dexclassdataobject {
	backuppointer := d.pointer
	d.pointer = start
	staticfieldsize := d.readuleb128()
	instancefieldsize := d.readuleb128()
	virtualmethodsize := d.readuleb128()
	directmethodsize := d.readuleb128()
	data := dexclassdataobject{
		staticfieldsize:   uleb128(staticfieldsize),
		instancefieldsize: uleb128(instancefieldsize),
		directmethodsize:  uleb128(directmethodsize),
		virtualmethodsize: uleb128(virtualmethodsize),
		staticfields:      d.parseencodedfield(staticfieldsize),
		instancefields:    d.parseencodedfield(instancefieldsize),
		directmethods:     d.parseencodedmethod(directmethodsize),
		virtualmethods:    d.parseencodedmethod(virtualmethodsize),
	}
	d.pointer = backuppointer
	return data
}

func (d *dex) parseclass(start uint32, size uint32) {
	backuppointer := d.pointer
	d.pointer = start
	for element := uint32(0); element < size; {
		element++
		classindex := d.readuint32()
		accessflag := d.readuint32()
		superclassindex := d.readuint32()
		interfaceoffset := d.readuint32()
		sourcefileindex := d.readuint32()
		annotationoffset := d.readuint32()
		classdataoffset := d.readuint32()
		staticvalueoffset := d.readuint32()
		classdataitem := dexclassdataobject{}
		if classdataoffset > 0 {
			classdataitem = d.parseclassdataitem(classdataoffset)
		}

		data := dexclassdataitem{
			classindex:        classindex,
			accessflag:        accessflag,
			superclassindex:   superclassindex,
			interfaceoffset:   interfaceoffset,
			sourcefileindex:   sourcefileindex,
			annotationoffset:  annotationoffset,
			classdataoffset:   classdataoffset,
			staticvalueoffset: staticvalueoffset,
			classdataitem:     classdataitem,
			classitem:         d.typetable[classindex],
			superclassitem:    d.typetable[superclassindex],
		}
		d.classtable = append(d.classtable, data)
	}
	d.pointer = backuppointer
}

func AppendIfMissing(slice []string, i string) []string {
	for _, ele := range slice {
		if ele == i {
			return slice
		}
	}
	return append(slice, i)
}

func (d *dex) parse() []string {
	d.header.magic = d.readbytes(8)
	d.header.version, _ = strconv.ParseInt(string(d.header.magic[4:7]), 10, 32)
	d.header.checksum = d.readuint32()
	d.header.signature = hex.EncodeToString(d.readbytes(20))
	d.header.filesize = d.readuint32()
	d.header.headersize = d.readuint32()
	d.header.endiantag = d.readuint32()
	d.header.linksize = d.readuint32()
	d.header.linkoffset = d.readuint32()
	d.header.mapoffset = d.readuint32()
	d.header.stringidssize = d.readuint32()
	d.header.stringidsoffset = d.readuint32()
	d.header.typeidssize = d.readuint32()
	d.header.typeidsoffset = d.readuint32()
	d.header.protoidssize = d.readuint32()
	d.header.protoidsoffset = d.readuint32()
	d.header.fieldidssize = d.readuint32()
	d.header.fieldidsoffset = d.readuint32()
	d.header.methodidssize = d.readuint32()
	d.header.methodidsoffset = d.readuint32()
	d.header.classdefsize = d.readuint32()
	d.header.classdefoffset = d.readuint32()
	d.header.datasize = d.readuint32()
	d.header.dataoffset = d.readuint32()
	if d.header.headersize != 0x70 {
		log.Fatalf("Invalid header size , expect 0x70 , found: 0x%x", d.header.headersize)
	}
	if d.header.endiantag != 0x12345678 {
		if d.header.endiantag != 0x78563412 {
			log.Fatalf("Invalid endian tag , expect 0x12345678 | 0x78563412 , found: 0x%x", d.header.endiantag)
		}
	}
	if d.header.linksize == 0 && d.header.linkoffset != 0 {
		log.Fatalf("Mismatched link size and linkoffset , should be 0x0, found: 0x%x", d.header.linkoffset)
	}

	d.parsestring(d.header.stringidsoffset, d.header.stringidssize)
	d.parsetype(d.header.typeidsoffset, d.header.typeidssize)
	d.parseproto(d.header.protoidsoffset, d.header.protoidssize)
	d.parsefield(d.header.fieldidsoffset, d.header.fieldidssize)
	d.parsemethod(d.header.methodidsoffset, d.header.methodidssize)
	d.parseclass(d.header.classdefoffset, d.header.classdefsize)

	values := []string{}

	for _, k := range d.classtable {

		slices := strings.Split(k.classitem.data.value[1:], "/")
		value := strings.Join(slices[:len(slices)-1], ".")
		values = AppendIfMissing(values, value)

	}

	return values

	// fmt.Println("Superclass: ", k.superclassitem.data.value)
	// fmt.Println("Fields: ", k.classdataitem.staticfieldsize)
	// for _, n := range k.classdataitem.staticfields {
	// fmt.Println("Field: ", n.fielditem.nameitemdata.value)
	// }
	// fmt.Println("Methods: ", k.classdataitem.directmethodsize+k.classdataitem.virtualmethodsize)
	// for _, j := range k.classdataitem.directmethods {
	// 	fmt.Println("Direct Method Name: ", j.methoditem.nameitemdata.value)
	// 	fmt.Println("Shorty: ", j.methoditem.protoitemdata.shorty.value)
	// 	fmt.Println("Return : ", j.methoditem.protoitemdata.returntype.data.value)
	// 	for _, q := range j.methoditem.protoitemdata.parameterstypelist.list {
	// 		fmt.Println("Param: ", q.typedataitem.data.value)
	// 	}
	// }
	// for _, j := range k.classdataitem.virtualmethods {
	// 	fmt.Println("Virtual Method Name: ", j.methoditem.nameitemdata.value)
	// 	fmt.Println("Shorty: ", j.methoditem.protoitemdata.shorty.value)
	// 	fmt.Println("Return : ", j.methoditem.protoitemdata.returntype.data.value)
	// 	for _, q := range j.methoditem.protoitemdata.parameterstypelist.list {
	// 		fmt.Println("Param: ", q.typedataitem.data.value)
	// 	}
	// }
}

func main() {
	d := new(dex)
	values := d.new("classes.dex")

	for _, v := range values {
		fmt.Println(v)
	}
}

//export getlib
func getlib(dexfile string) *C.char {

	var str strings.Builder
	// var ret []*C.char

	defer func() {
		if r := recover(); r != nil {
			fmt.Println("Recovered from error in dex parsing")
		}
	}()

	d := new(dex)
	data := d.new(dexfile)

	// Workaround because SLICES don't work for me :(
	for i := 0; i < len(data); i++ {
		str.WriteString(data[i])
		str.WriteString("\n")
	}
	return C.CString(str.String())

}
