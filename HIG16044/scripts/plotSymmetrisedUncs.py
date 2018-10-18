#!/usr/bin/env python
import sys
import ROOT
import math
from functools import partial
import CombineHarvester.CombineTools.plotting as plot
import json
import argparse
import os.path
from array import array

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)
plot.ModTDRStyle()
ROOT.gStyle.SetTickLength(0., "Y")
ROOT.gStyle.SetEndErrorSize(5)

xvals=[]
yvals_s1=[]
yvals_s2=[]
yvals_statonly=[]

xvals.append(300.0)
yvals_s1.append(0.143)
yvals_s2.append(0.123)
yvals_statonly.append(0.099)

xvals.append(3000.0)
yvals_s1.append(0.074)
yvals_s2.append(0.052)
yvals_statonly.append(0.032)

gr_s1= ROOT.TGraphAsymmErrors(2)
gr_s2= ROOT.TGraphAsymmErrors(2)
gr_stat= ROOT.TGraphAsymmErrors(2)

plot.Set(gr_s1, LineColor=ROOT.kGreen+3, MarkerSize=0, LineWidth=2)
plot.Set(gr_s2, LineColor=ROOT.kRed, MarkerSize=0, LineWidth=2)
plot.Set(gr_stat, LineColor=ROOT.kBlue, MarkerSize=0, LineWidth=2)

gr_s1.SetPoint(0, 0, 0.625)
gr_s1.SetPointError(0,0,0.143,0,0)
gr_s1.SetPoint(1, 0, 0.375)
gr_s1.SetPointError(1,0,0.074,0,0)

gr_s2.SetPoint(0, 0, 0.625)
gr_s2.SetPointError(0,0,0.123,0,0)
gr_s2.SetPoint(1, 0, 0.375)
gr_s2.SetPointError(1,0,0.052,0,0)

gr_stat.SetPoint(0, 0, 0.625)
gr_stat.SetPointError(0,0,0.099,0,0)
gr_stat.SetPoint(1, 0, 0.375)
gr_stat.SetPointError(1,0,0.032,0,0)


canv = ROOT.TCanvas('c1', 'c1',400,300)
pads = plot.OnePad()
pads[0].SetTicky(0)

axis = ROOT.TH2F('axis','',1,0,0.27,4,0,1)
plot.Set(axis.GetXaxis(), Title = 'Expected uncertainty on #mu_{VHbb}')
axis.GetYaxis().SetBinLabel(3, '300 fb^{-1}')
axis.GetYaxis().SetBinLabel(2, '3000 fb^{-1}')
axis.GetYaxis().LabelsOption('v')
plot.Set(axis.GetYaxis(), LabelSize=0.07)

axis.Draw()

gr_s1.Draw('SAMEP')
gr_s2.Draw("SAMEP")
gr_stat.Draw("SAMEP")

latex = ROOT.TLatex()
plot.Set(latex, TextAlign=12,TextSize=0.035)
latex.SetTextFont(42)
txt_dict = {
'300': '0.10 (Stat); 0.12 (S2); 0.14 (S1)',
'3000': '0.03 (Stat); 0.05 (S2); 0.07 (S1)'
}

latex.DrawLatex(0.16,0.625,txt_dict['300'])
latex.DrawLatex(0.16,0.375,txt_dict['3000'])



legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.93, '', 'NBNDC')
legend.AddEntry(gr_s1, 'YR2018 S1', 'L')
legend.AddEntry(gr_s2, 'YR2018 S2', 'L')
legend.AddEntry(gr_stat, 'Stat Only', 'L')
legend.Draw()


plot.DrawCMSLogo(pads[0],'CMS','Projection',11,0.045,0.03,1.0,'',1.0)
plot.DrawTitle(pads[0],'#sqrt{s} = 13 TeV',3)
canv.SaveAs('Uncert300and3000.pdf')
canv.Print('Uncert300and3000.png')

