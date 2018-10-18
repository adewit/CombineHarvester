#!/usr/bin/env python

import CombineHarvester.CombineTools.ch as ch
import CombineHarvester.HIG16044.systematics as systs
import ROOT as R
import glob
import numpy as np
import os
import sys
import argparse

def adjust_shape(proc,nbins):
  new_hist = proc.ShapeAsTH1F();
  new_hist.Scale(proc.rate())
  for i in range(1,new_hist.GetNbinsX()+1-nbins):
    new_hist.SetBinContent(i,0.)
  proc.set_shape(new_hist,True)


parser = argparse.ArgumentParser()
parser.add_argument(
 '--channel', default='all', help="""Which channels to run? Supported options: 'all', 'Znn', 'Zee', 'Zmm', 'Zll', 'Wen', 'Wmn','Wln'""")
parser.add_argument(
 '--output_folder', default='vhbb2016', help="""Subdirectory of ./output/ where the cards are written out to""")
parser.add_argument(
 '--auto_rebin', action='store_true', help="""Rebin automatically?""")
parser.add_argument(
 '--bbb_mode', default=6, type=int, help="""Sets the type of bbb uncertainty setup. 0: no bin-by-bins, 1: bbb's as in 2016 analysis, 2: Use the CH bbb factory to add bbb's, 3: as 2 but with new CMSHistFunc, 4: autoMCstats , 5 : bbb's as in 2016 analysis with new CMSHistFunc (just for testing) 6: no bbb's but new CMSHistFunc""")
parser.add_argument(
  '--inc_beff', default=1, type=float, help="""increase in b-tagging efficiency""")
parser.add_argument(
 '--zero_out_low', action='store_true', help="""Zero-out lowest SR bins (purely for the purpose of making yield tables""")
parser.add_argument(
 '--Zmm_fwk', default='Xbb', help="""Framework the Zmm inputs were produced with. Supported options: 'Xbb', 'AT'""")
parser.add_argument(
 '--Zee_fwk', default='Xbb', help="""Framework the Zee inputs were produced with. Supported options: 'Xbb', 'AT'""")
parser.add_argument(
 '--Wmn_fwk', default='AT', help="""Framework the Wmn inputs were produced with. Supported options: 'Xbb', 'AT'""")
parser.add_argument(
 '--Wen_fwk', default='AT', help="""Framework the Wen inputs were produced with. Supported options: 'Xbb', 'AT'""")
parser.add_argument(
 '--Znn_fwk', default='Xbb', help="""Framework the Znn inputs were produced with. Supported options: 'Xbb', 'AT'""")


args = parser.parse_args()

cb = ch.CombineHarvester()

shapes = os.environ['CMSSW_BASE'] + '/src/CombineHarvester/HIG16044/shapes/'

mass = ['125']

chns = []

if args.channel=="all":
  chns = ['Wen','Wmn','Znn','Zee','Zmm']
if 'Zll' in args.channel or 'Zmm' in args.channel:
  chns.append('Zmm')
if 'Zll' in args.channel  or 'Zee' in args.channel:
  chns.append('Zee')
if 'Wln' in args.channel or 'Wmn' in args.channel:
  chns.append('Wmn')
if 'Wln' in args.channel or 'Wen' in args.channel:
  chns.append('Wen')
if 'Znn' in args.channel:
  chns.append('Znn')

input_fwks = {
  'Wen' : args.Wen_fwk, 
  'Wmn' : args.Wmn_fwk,
  'Zee' : args.Zee_fwk,
  'Zmm' : args.Zmm_fwk,
  'Znn' : args.Znn_fwk
}

for chn in chns:
  if not input_fwks[chn]=='Xbb' and not input_fwks[chn]=='AT':
    print "Framework ", input_fwks[chn], "not supported! Choose from: 'Xbb','AT'"
    sys.exit()

#The following in anticipation of separate subdirs for Xbb and AT inputs
folder_map = {
  'Xbb' : 'Example',
  'AT'  : 'Example'
}

input_folders = {
  'Wen' : folder_map[input_fwks['Wen']],
  'Wmn' : folder_map[input_fwks['Wmn']],
  'Zee' : folder_map[input_fwks['Zee']],
  'Zmm' : folder_map[input_fwks['Zmm']],
  'Znn' : folder_map[input_fwks['Znn']] 
}

bkg_procs = {
  'Wen' : ['s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],
  'Wmn' : ['s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],
  'Zmm' : ['s_Top','TT','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],
  'Zee' : ['s_Top','TT','VVHF','VVLF','Zj0b','Zj1b','Zj2b'],
  'Znn' : ['s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b','QCD']
}

sig_procs = {
  'Wen' : ['WH_hbb','ZH_hbb'],
  'Wmn' : ['WH_hbb','ZH_hbb'],
  'Zmm' : ['ZH_hbb','ggZH_hbb'],
  'Zee' : ['ZH_hbb','ggZH_hbb'],
  'Znn' : ['ZH_hbb','ggZH_hbb','WH_hbb']
}

sig_procs_ren = {
  'Wen' : ['WH_lep','ZH_hbb'],
  'Wmn' : ['WH_lepb','ZH_hbb'],
  'Zmm' : ['ZH_hbb','ggZH_hbb'],
  'Zee' : ['ZH_hbb','ggZH_hbb'],
  'Znn' : ['ZH_hbb','ggZH_hbb','WH_lep']
}


cats = {
  'Zee' : [
    (1, 'ZeeHighPt_13TeV'), (2, 'ZeeLowPt_13TeV'), (3, 'Zlf_high_Zee'), (4,'Zlf_low_Zee'),
    (5, 'Zhf_high_Zee'), (6, 'Zhf_low_Zee'), (7,'ttbar_high_Zee'), (8,'ttbar_low_Zee')
  ],
  'Zmm' : [
    (1, 'ZuuHighPt_13TeV'), (2, 'ZuuLowPt_13TeV'), (3, 'Zlf_high_Zuu'), (4,'Zlf_low_Zuu'),
    (5, 'Zhf_high_Zuu'), (6, 'Zhf_low_Zuu'), (7,'ttbar_high_Zuu'), (8,'ttbar_low_Zuu')
  ],
  'Znn' : [
    (1, 'Znn_13TeV_Signal'), (3, 'Znn_13TeV_Zlight'), (5, 'Znn_13TeV_Zbb'), (7,'Znn_13TeV_TT')
  ],
 'Wen' : [
    (1, 'WenHighPt'), (3,'wlfWen'), (5,'whfWenHigh'), (6,'whfWenLow'), (7,'ttWen')
  ],
 'Wmn' : [
    (1, 'WmnHighPt'), (3,'wlfWmn'), (5,'whfWmnHigh'), (6,'whfWmnLow'), (7,'ttWmn')
  ]

}

for chn in chns:
  cb.AddObservations( ['*'], ['vhbb'], ['13TeV'], [chn], cats[chn])
  cb.AddProcesses( ['*'], ['vhbb'], ['13TeV'], [chn], bkg_procs[chn], cats[chn], False)
  cb.AddProcesses( ['*'], ['vhbb'], ['13TeV'], [chn], sig_procs[chn], cats[chn], True)

systs.AddSystematics(cb)

cb.cp().AddSyst(cb,'rate_lumiscale','rateParam', ch.SystMap()(1.0))


if args.bbb_mode==1 or args.bbb_mode==5:
  systs.AddBinByBinSystematics(cb)

  if args.bbb_mode==5:
    cb.AddDatacardLineAtEnd("* autoMCStats -1")



for chn in chns:
  file = shapes + input_folders[chn] + "/vhbb_"+chn+".root"
  if input_fwks[chn] == 'Xbb':
    cb.cp().channel([chn]).backgrounds().ExtractShapes(
      file, '$BIN/$PROCESS', '$BIN/$PROCESS$SYSTEMATIC')
    cb.cp().channel([chn]).signals().ExtractShapes(
      file, '$BIN/$PROCESS', '$BIN/$PROCESS$SYSTEMATIC')
      #file, '$BIN/$PROCESS$MASS', '$BIN/$PROCESS$MASS_$SYSTEMATIC')
  elif input_fwks[chn] == 'AT':
    cb.cp().channel([chn]).backgrounds().ExtractShapes(
      file, 'BDT_$BIN_$PROCESS', 'BDT_$BIN_$PROCESS_$SYSTEMATIC')
    cb.cp().channel([chn]).signals().ExtractShapes(
      file, 'BDT_$BIN_$PROCESS', 'BDT_$BIN_$PROCESS_$SYSTEMATIC')


#To rename processes:
#cb.cp().ForEachObj(lambda x: x.set_process("WH_lep") if x.process()=='WH_hbb' else None)

rebin = ch.AutoRebin().SetBinThreshold(0.).SetBinUncertFraction(1.0).SetRebinMode(1).SetPerformRebin(True).SetVerbosity(1)

if args.auto_rebin:
  rebin.Rebin(cb, cb)

if args.bbb_mode==2 or args.bbb_mode==3:
  print "Generating bbb uncertainties..."
  bbb = ch.BinByBinFactory()
  bbb.SetAddThreshold(0.).SetMergeThreshold(0.4).SetFixNorm(False)
  for chn in chns:
    print " - Doing bbb for channel ", chn
    bbb.MergeAndAdd(cb.cp().channel([chn]).process(['s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b','QCD']),cb)
#    bbb.MergeAndAdd(cb.cp().channel([chn]).bin_id([1,2]).process(['s_Top','TT','Wj0b','Wj1b','Wj2b','VVHF','VVLF','Zj0b','Zj1b','Zj2b','QCD']),cb)
  if args.bbb_mode==3:
    cb.AddDatacardLineAtEnd("* autoMCStats -1")
    
if args.bbb_mode==4:
  cb.AddDatacardLineAtEnd("* autoMCStats 0")

if args.bbb_mode==6:
  cb.AddDatacardLineAtEnd("* autoMCStats -1")


cb.SetGroup('sigTheory',['CMS_vhbb_boost.*','BR_hbb','QCDscale_VH','QCDscale_ggZH','CMS_vhbb_boost_.*','CMS_vhbb_LHE_weights.*WH','CMS_vhbb_LHE_weights.*ZH','pdf_Higgs_gg','pdf_Higgs_qqbar','CMS_vhbb_EWK_Zll'])
cb.SetGroup('bkgTheory',['CMS_vhbb_LHE_weights_pdf_TT','CMS_vhbb_LHE_weights_pdf_VVHF','CMS_vhbb_LHE_weights_pdf_VVLF','CMS_vhbb_LHE_weights_pdf_Wj0b','CMS_vhbb_LHE_weights_pdf_Wj1b','CMS_vhbb_LHE_weights_pdf_Zj0b','CMS_vhbb_LHE_weights_pdf_Zj1b','CMS_vhbb_LHE_weights_pdf_Zj2b','CMS_vhbb_LHE_weights_scale_mu.*scale_QCD','CMS_.*scale_mu.*TT','CMS_.*scale_mu.*VVHF','CMS_.*scale_mu.*VVLF','CMS_.*scale_mu.*0b','CMS_.*scale_mu.*1b','CMS_.*scale_mu.*2b','QCDscale_VV','QCDscale_ttbar','pdf_gg','pdf_qqbar','CMS_vhbb_VV','CMS_vhbb_ST','CMS_vhbb_puWeight'])
#cb.SetGroup('expt',['lumi_13TeV','CMS_vhbb_eff_.*','CMS_vhbb_trigger_MET_13TeV','CMS_vhbb_res_j_.*','CMS_vhbb_scale_j_.*','CMS_vhbb_bTagWeight.*'])
cb.SetGroup('pBTag',['CMS_vhbb_bTagWeightHF_.*','CMS_vhbb_bTagWeightJES_.*','CMS_vhbb_bTagWeightLF_.*','CMS_vhbb_bTagWeightcErr.*'])
cb.SetGroup('pBTagStat',['CMS_vhbb_bTagWeightHFStats.*','CMS_vhbb_bTagWeightLFStats.*'])
cb.SetGroup('pLumi',['lumi_13TeV'])
cb.SetGroup('pScaleJAbs',['CMS_vhbb_scale_j_Absolute.*','CMS_vhbb_scale_j_Fragmentation_13TeV','CMS_vhbb_scale_j_SinglePion.*'])
cb.SetGroup('pScaleJRel',['CMS_vhbb_scale_j_Relative.*'])
cb.SetGroup('pScaleJPileup',['CMS_vhbb_scale_j_PileUp.*'])
cb.SetGroup('pScaleJTime',['CMS_vhbb_scale_j_TimePtEta.*'])
cb.SetGroup('pScaleJFlav',['CMS_vhbb_scale_j_FlavorQCD_13TeV'])
cb.SetGroup('pResJ',['CMS_res_j'])
cb.SetGroup('pEleID',['CMS_vhbb_eff_e_MVAID_Zll_13TeV','CMS_vhbb_eff_e_Wln_13TeV','CMS_vhbb_eff_e_tracker_Zll_13TeV'])
cb.SetGroup('pMuonID',['CMS_vhbb_eff_m_ISO_Zll_13TeV','CMS_vhbb_eff_m_MVAID_Zll_13TeV','CMS_vhbb_eff_m_Wln_13TeV','CMS_vhbb_eff_m_tracker_Zll_13TeV'])
cb.SetGroup('unassigned',['CMS_vhbb_eff_e_trigger_Zll_13TeV','CMS_vhbb_eff_m_trigger_Zll_13TeV','CMS_vhbb_trigger_MET_13TeV','CMS_vhbb_ptwweights_tt','CMS_vhbb_ptwweights_whf','CMS_vhbb_ptwweights_wlf'])

print args.inc_beff
cb.cp().process(['Zj2b','Wj2b','TT','VVHF','WH_hbb','ZH_hbb','ggZH_hbb']).ForEachProc(lambda x: x.set_rate(x.rate()*args.inc_beff*args.inc_beff))
cb.cp().process(['Zj1b','Wj1b','s_Top']).ForEachProc(lambda x: x.set_rate(x.rate()*args.inc_beff))


if args.zero_out_low:
  nbins_to_keep = {'Wen':[[1,5]],'Wmn':[[1,5]],'Znn':[[1,5]],'Zee':[[1,5],[2,3]],'Zmm':[[1,5],[2,3]]}
  for chn in chns:
    for i in range(len(nbins_to_keep[chn])):
      print nbins_to_keep[chn][i]
      cb.cp().channel([chn]).bin_id([nbins_to_keep[chn][i][0]]).ForEachProc(lambda x: adjust_shape(x,nbins_to_keep[chn][i][1]))
      cb.cp().channel([chn]).bin_id([nbins_to_keep[chn][i][0]]).ForEachObs(lambda x: adjust_shape(x,nbins_to_keep[chn][i][1]))

ch.SetStandardBinNames(cb)

writer=ch.CardWriter("output/" + args.output_folder + "/$TAG/$BIN.txt",
                      "output/" + args.output_folder + "/$TAG/vhbb_input.root")
writer.SetWildcardMasses([])
writer.SetVerbosity(1);
                
#Combined:
writer.WriteCards("cmb",cb);

#Per channel:
for chn in chns:
  writer.WriteCards(chn,cb.cp().channel([chn]))

#Zll and Wln:
if 'Wen' in chns and 'Wmn' in chns:
  writer.WriteCards("Wln",cb.cp().channel(['Wen','Wmn']))

if 'Zee' in chns and 'Zmm' in chns:
  writer.WriteCards("Zll",cb.cp().channel(['Zee','Zmm']))
