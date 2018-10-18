#!/usr/bin/env python

import CombineHarvester.CombineTools.plotting as plot
import ROOT
import argparse
import json

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)
plot.ModTDRStyle()
ROOT.gStyle.SetTickLength(0., "Y")
ROOT.gStyle.SetEndErrorSize(5)


parser = argparse.ArgumentParser()
parser.add_argument('--inputs1',help = 'input json file for s1')
parser.add_argument('--inputs2',help = 'input json file for s2')
parser.add_argument('--inputstat',help = 'input json file for stat only')
parser.add_argument('--output','-o', help = 'Output filename')

args = parser.parse_args()

with open(args.inputs1) as jsonfiles1:
  jss1 = json.load(jsonfiles1)

with open(args.inputs2) as jsonfiles2:
  jss2 = json.load(jsonfiles2)

with open(args.inputstat) as jsonfilestat:
  jsstat = json.load(jsonfilestat)


canv = ROOT.TCanvas(args.output,args.output)
pads = plot.OnePad()
pads[0].SetTicks(1,-1)
pads[0].SetLeftMargin(0.22)
pads[0].SetTicky(0)

axis = ROOT.TH2F('axis', '',1,0,0.5,7,0,7)
plot.Set(axis.GetYaxis(), LabelSize=0)
plot.Set(axis.GetXaxis(), Title = 'Expected uncertainty')
axis.Draw()


#cmb_band = ROOT.TBox()
#plot.Set(cmb_band, FillColor=ROOT.kGreen)
#plot.DrawVerticalBand(pads[0],cmb_band,js['r']['val']-js['r']['ErrLo'],js['r']['val']+js['r']['ErrHi'])

#cmb_line = ROOT.TLine()
#plot.Set(cmb_line,LineWidth=2)
#plot.DrawVerticalLine(pads[0],cmb_line,js['r']['val'])

horizontal_line = ROOT.TLine()
plot.Set(horizontal_line,LineWidth=2,LineStyle=2)
plot.DrawHorizontalLine(pads[0],horizontal_line,3)



gr_s1 = ROOT.TGraphAsymmErrors(5)
gr_s2 = ROOT.TGraphAsymmErrors(5)
gr_stat = ROOT.TGraphAsymmErrors(5)
plot.Set(gr_s1, LineWidth=2, LineColor=ROOT.kGreen+3, MarkerSize=0)
plot.Set(gr_s2, LineWidth=2, LineColor=ROOT.kRed, MarkerSize=0)
plot.Set(gr_stat, LineWidth=2, LineColor=ROOT.kBlue, MarkerSize=0)

y_pos = 4.5
x_text = -0.1
x_text_after = 0.25
i=0
latex = ROOT.TLatex()
plot.Set(latex, TextAlign=12,TextSize=0.035)
latex.SetTextFont(42)
latex_after = ROOT.TLatex()
latex_after.SetTextFont(42)
plot.Set(latex_after, TextAlign=12,TextSize=0.028)
order = ['r_ZH','r_WH','r_zerolep','r_onelep','r_twolep']
txt_dict = {
  'r_ZH': 'ZH(bb)',
  'r_WH': 'WH(bb)',
  'r_zerolep': '0 lept.',
  'r_onelep': '1 lept.',
  'r_twolep': '2 lept.',
}
txt_dict_after = {
  'r_ZH': '%.2f (Stat); %.2f (S2); %.2f (S1)'%((jsstat['r_ZH']['ErrHi']+jsstat['r_ZH']['ErrLo'])/2.,(jss2['r_ZH']['ErrHi']+jss2['r_ZH']['ErrLo'])/2.,(jss1['r_ZH']['ErrHi']+jss1['r_ZH']['ErrLo'])/2.),
  'r_WH': '%.2f (Stat); %.2f (S2); %.2f (S1)'%((jsstat['r_WH']['ErrHi']+jsstat['r_WH']['ErrLo'])/2.,(jss2['r_WH']['ErrHi']+jss2['r_WH']['ErrLo'])/2.,(jss1['r_WH']['ErrHi']+jss1['r_WH']['ErrLo'])/2.),
  'r_zerolep': '%.2f (Stat); %.2f (S2); %.2f (S1)'%((jsstat['r_zerolep']['ErrHi']+jsstat['r_zerolep']['ErrLo'])/2.,(jss2['r_zerolep']['ErrHi']+jss2['r_zerolep']['ErrLo'])/2.,(jss1['r_zerolep']['ErrHi']+jss1['r_zerolep']['ErrLo'])/2.),
  'r_onelep': '%.2f (Stat); %.2f (S2); %.2f (S1)'%((jsstat['r_onelep']['ErrHi']+jsstat['r_onelep']['ErrLo'])/2.,(jss2['r_onelep']['ErrHi']+jss2['r_onelep']['ErrLo'])/2.,(jss1['r_onelep']['ErrHi']+jss1['r_onelep']['ErrLo'])/2.),
  'r_twolep': '%.2f (Stat); %.2f (S2); %.2f (S1)'%((jsstat['r_twolep']['ErrHi']+jsstat['r_twolep']['ErrLo'])/2.,(jss2['r_twolep']['ErrHi']+jss2['r_twolep']['ErrLo'])/2.,(jss1['r_twolep']['ErrHi']+jss1['r_twolep']['ErrLo'])/2.),
}


for stre in order:
  gr_s1.SetPoint(i,0,y_pos)
  gr_s1.SetPointError(i,0,(jss1[stre]['ErrLo']+jss1[stre]['ErrHi'])/2.,0,0)
  gr_s2.SetPoint(i,0,y_pos)
  gr_s2.SetPointError(i,0,(jss2[stre]['ErrLo']+jss2[stre]['ErrHi'])/2.,0,0)
  gr_stat.SetPoint(i,0,y_pos)
  gr_stat.SetPointError(i,0,(jsstat[stre]['ErrLo']+jsstat[stre]['ErrHi'])/2.,0,0)
  latex.DrawLatex(x_text,y_pos,txt_dict[stre])
  latex_after.DrawLatex(x_text_after,y_pos,txt_dict_after[stre])

  i+=1
  y_pos -= 1.

gr_s1.Draw("SAMEP")
gr_s2.Draw("SAMEP")
gr_stat.Draw("SAMEP")

legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.93, '', 'NBNDC')
legend.AddEntry(gr_s1, 'YR2018 S1', 'L')
legend.AddEntry(gr_s2, 'YR2018 S2', 'L')
legend.AddEntry(gr_stat, 'Stat Only', 'L')
legend.Draw()


pads[0].cd()
pads[0].GetFrame().Draw()
pads[0].RedrawAxis()

plot.DrawCMSLogo(pads[0],'CMS','Projection',11,0.045,0.05,1.0,'',1.0)
plot.DrawTitle(pads[0],'3000 fb^{-1} (13 TeV)',3)

latex.SetTextFont(42)
latex.SetTextSize(0.03)
#latex.DrawLatex(0.08,5.5,"pp#rightarrow VH; H#rightarrow b#bar{b}")
#latex.DrawLatex(0.08,5.1,"Combined #mu=%.1f#pm%.2f"%(js['r']['val'],js['r']['ErrHi']))

canv.Print('.png')
canv.Print('.pdf')
