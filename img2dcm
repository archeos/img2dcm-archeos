#!/usr/bin/env python

#--------------------------------------------------------------------------
# Software:     img2dcm
# Copyright:    (C) 2001  Centro de Pesquisas Renato Archer
# Homepage:     https://bitbucket.org/tfmoraes/img2dcm
# Contact:      invesalius@cti.gov.br
# License:      GNU - GPL 2 (LICENSE.txt/LICENCA.txt)
#--------------------------------------------------------------------------
#    Este programa e software livre; voce pode redistribui-lo e/ou
#    modifica-lo sob os termos da Licenca Publica Geral GNU, conforme
#    publicada pela Free Software Foundation; de acordo com a versao 2
#    da Licenca.
#
#    Este programa eh distribuido na expectativa de ser util, mas SEM
#    QUALQUER GARANTIA; sem mesmo a garantia implicita de
#    COMERCIALIZACAO ou de ADEQUACAO A QUALQUER PROPOSITO EM
#    PARTICULAR. Consulte a Licenca Publica Geral GNU para obter mais
#    detalhes.
#--------------------------------------------------------------------------
import glob
import os.path
import random
import re
import tempfile
import time

import gdcm
import ivDicom
import vtk
import vtkgdcm

from optparse import OptionParser

def parse_cmd_line():
    parser = OptionParser()
    parser.add_option('-i', '--input', dest='input', 
                      help='A dicom file or directory with dicom files')

    parser.add_option('-o', '--output', dest='output', 
                      help='Output file or directory')

    parser.add_option('-s', '--spacing', dest='spacing', type="float", nargs=3,
                      default = (1, 1, 1), help='Spacing x, y and z')

    parser.add_option('-m', '--modality', dest='modality', default="CT",
                      help='Modality')

    parser.add_option('-t', '--type', dest='type', default="bmp",
                      help='Type of image input', 
                      choices = ("bmp", "tif", "png", "jpg", "vti"))

    parser.add_option('-p', '--patient', dest='patient', default="",
                      help='Patient')

    parser.add_option('--serie', dest='serie', default=1, type = "int",
                      help='Serie number')

    parser.add_option('--institution', dest='institution', default="",
                      help='Institution')

    options, args = parser.parse_args()

    print options

    return options

class Img2Dcm(object):
    def __init__(self, patient, institution, modality, serie, spacing):

        self.patient = patient
        self.institution = institution
        self.modality = modality
        self.serie = serie
        self.spacing = spacing
        self.patient_id = gdcm.UIDGenerator().Generate() #int(random.random() * 10000)
        self.study_uid = gdcm.UIDGenerator().Generate() #int(random.random() * 10000)
        self.study_id = str(int(random.random() * 10000))
        self.series_uid = gdcm.UIDGenerator().Generate() #int(random.random() * 10000)

    def img2dcm(self, input_img, output, img_type, img_number): 

        if img_type == "jpg":
            print "JPG"
            image = vtk.vtkJPEGReader()
            image.SetFileName(input_img)
            image.Update()
            
        elif img_type == "tif":
            print "TIF"
            image = vtk.vtkTIFFReader()
            image.SetFileName(input_img)
            image.Update()
            
        elif img_type == "bmp":
            print "BMP"
            image = vtk.vtkBMPReader()
            image.SetFileName(input_img)
            image.Allow8BitBMPOn()
            image.Update()
            
        elif img_type == "png": 
            print "PNG"
            image = vtk.vtkPNGReader()
            image.SetFileName(input_img)
            image.SetDataSpacing(self.spacing)
            image.Update()

        elif img_type == "vti": 
            print "VTI"
            image = vtk.vtkXMLImageDataReader()
            image.SetFileName(input_img)
            image.Update()
        
            #if (orientation == 0):
        image_pos = img_number * self.spacing[2]
        image_localization = image_pos

        # print image_pos, img_number, image.GetOutput().GetScalarRange()

        img_clone = vtk.vtkImageData()
        img_clone.DeepCopy(image.GetOutput())
        img_clone.SetSpacing(self.spacing)
        img_clone.Update()

        # v = vtk.vtkImageViewer()
        # v.SetInput(image.GetOutput())
        # v.SetColorLevel(500)
        # v.SetColorWindow(240)
        # v.Render()

        # time.sleep(3)

        # a = vtk.vtkImageCast()
        # a.SetOutputScalarTypeToUnsignedChar()
        # a.SetInput(image.GetOutput())
        # a.ClampOverflowOn()
        # a.Update()

        #b = vtk.vtkJPEGWriter()
        #b.SetFileName("C:\\teste.jpg")
        #b.SetInput(a.GetOutput())
        #b.writer()

        #spacing = image.GetOutput().GetSpacing()
        #elif (orientation == 1):
        #    image_pos[0] =  image_pos[0] + thickness
        #    image_localization = image_localization + thickness
        #    img_number = img_number + 1
        
        #elif (orientation == 2):
        #    image_pos[1] =  image_pos[1] + thickness
        #    image_localization = image_localization + thickness
        #    img_number = img_number + 1
        pos = 0, 0, image_pos
        print pos

        # transform = vtk.vtkTransform()
        # transform.Translate(pos)

        # transform_filter = vtk.vtkImageReslice()
        # transform_filter.SetInput(image.GetOutput())
        # transform_filter.SetResliceTransform(transform)
        # transform_filter.Update()

        properties = vtk.vtkMedicalImageProperties()
        properties.SetModality(self.modality)
        properties.SetInstitutionName(self.institution)
        properties.SetPatientName(self.patient)
        properties.SetSliceThickness(str(self.spacing[2]))
        properties.SetSeriesNumber(str(self.serie))
        properties.SetImageNumber(str(img_number))
        properties.SetPatientID(self.patient_id)
        properties.SetStudyID(self.study_id)
        properties.AddUserDefinedValue("Image Position (Patient)", "%.5f\\%.5f\\%.5f" %
                                       (pos[0], pos[1], pos[2]))
        properties.AddUserDefinedValue("Instance Number", str(img_number))
        print str(img_number), properties.GetNumberOfUserDefinedValues()

        writer = vtkgdcm.vtkGDCMImageWriter()
        writer.SetInput(img_clone)
        writer.SetStudyUID(self.study_uid)
        writer.SetSeriesUID(self.series_uid)
        writer.SetMedicalImageProperties(properties)
        writer.SetFileName(output)
        # writer.SetImageFormat(vtk.VTK_LUMINANCE)
        writer.SetFileDimensionality(3)
        writer.Write()
               
        reader = gdcm.Reader()
        reader.SetFileName(output)
        reader.Read()

        anon = gdcm.Anonymizer()
        anon.SetFile(reader.GetFile())
        anon.Replace(gdcm.Tag(0x0020, 0x0013), str(img_number))
        anon.Replace(gdcm.Tag(0x0028, 0x0030), "%.6f\\%.6f" % (self.spacing[0],
                                                               self.spacing[1]))

        writer = gdcm.Writer()
        writer.SetFile(reader.GetFile())
        writer.SetFileName(output)
        writer.Write()    

        # print spacing, pos, image.GetOutput().GetScalarRange()

        # writer = ivDicom.DicomWriter()
        # writer.SetFileName(output)
        # writer.SaveIsNew(image.GetOutput())
        # 
        # writer.SetAcquisitionModality(self.modality)
        # writer.SetInstitutionName(self.institution)
        # writer.SetStudyID(self.study_uid)
        # writer.SetPatientID(self.patient_id)
        # writer.SetPatientName(self.patient)
        # writer.SetImageThickness(self.spacing[2])
        # writer.SetImageSeriesNumber(self.serie)
        # writer.SetImageNumber(img_number)
        # writer.SetImagePosition(pos)
        # writer.SetImageLocation(image_localization)
        # writer.SetPixelSpacing(self.spacing[:2])
        # writer.Save()

        print "Written", input_img, "->", output


def main():
    options = parse_cmd_line()

    input_file = options.input
    output = options.output
    spacing = options.spacing
    modality = options.modality
    image_type = options.type
    patient = options.patient
    serie = options.serie
    institution = options.institution
    # patient_id = gdcm.UIDGenerator().Generate() #int(random.random() * 10000)
    # study_uid = #int(random.random() * 10000)

    converter = Img2Dcm(patient, institution, modality, serie, spacing)

    if os.path.isfile(input_file):
        converter.img2dcm(input_file, output, image_type, 0)
    else:
        c_re = re.compile('\d+')

        if glob.has_magic(input_file):
            files = glob.glob(input_file)
        else:
            files = [f for f in glob.glob(os.path.join(input_file, '*')) \
                    if c_re.findall(f)]
        files.sort(key = lambda x: c_re.findall(x)[-1])

        if not os.path.exists(output):
            os.makedirs(output)

        for image_number, f in enumerate(files):
            output_file = os.path.join(output, "%04d.dcm" % image_number)
            converter.img2dcm(f, output_file, image_type, image_number)

if __name__ == '__main__':
    main()
