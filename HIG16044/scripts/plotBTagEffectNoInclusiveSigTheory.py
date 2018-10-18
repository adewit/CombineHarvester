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

xvals = []
yvals_s1 = []
yvals_s2 = []
yvals_s1_300 = []
yvals_s2_300 = []

xvals.append(0.85)
xvals.append(0.90)
xvals.append(0.95)
xvals.append(1.0)
xvals.append(1.05)
xvals.append(1.10)
xvals.append(1.15)

yvals_s1.append(0.080)
yvals_s1.append(0.077)
yvals_s1.append(0.075)
yvals_s1.append(0.073)
yvals_s1.append(0.072)
yvals_s1.append(0.070)
yvals_s1.append(0.069)

yvals_s1_noincsigth = [math.sqrt(x*x-0.046*0.046) for x in yvals_s1]

yvals_s2.append(0.058)
yvals_s2.append(0.055)
yvals_s2.append(0.053)
yvals_s2.append(0.051)
yvals_s2.append(0.050)
yvals_s2.append(0.048)
yvals_s2.append(0.047)

yvals_s2_noincsigth = [math.sqrt(x*x-0.022*0.022) for x in yvals_s2]

yvals_s1_300.append(0.162)
yvals_s1_300.append(0.155)
yvals_s1_300.append(0.148)
yvals_s1_300.append(0.143)
yvals_s1_300.append(0.137)
yvals_s1_300.append(0.132)
yvals_s1_300.append(0.128)

yvals_s1_noincsigth_300 = [math.sqrt(x*x-0.045*0.045) for x in yvals_s1_300]

yvals_s2_300.append(0.144)
yvals_s2_300.append(0.136)
yvals_s2_300.append(0.129)
yvals_s2_300.append(0.123)
yvals_s2_300.append(0.118)
yvals_s2_300.append(0.113)
yvals_s2_300.append(0.109)

yvals_s2_noincsigth_300 = [math.sqrt(x*x-0.022*0.022) for x in yvals_s2_300]

gr_s1_3000 = ROOT.TGraph(len(xvals), array('d', xvals), array('d', yvals_s1_noincsigth))
gr_s2_3000 = ROOT.TGraph(len(xvals), array('d', xvals), array('d', yvals_s2_noincsigth))
gr_s1_300 = ROOT.TGraph(len(xvals), array('d', xvals), array('d', yvals_s1_noincsigth_300))
gr_s2_300 = ROOT.TGraph(len(xvals), array('d', xvals), array('d', yvals_s2_noincsigth_300))
plot.Set(gr_s1_3000, LineColor=ROOT.kGreen+3, MarkerColor=ROOT.kGreen+3, LineWidth=2)
plot.Set(gr_s2_3000, LineColor=ROOT.kRed, MarkerColor=ROOT.kRed, LineWidth=2)
plot.Set(gr_s1_300, LineColor=ROOT.kGreen+3, MarkerColor=ROOT.kGreen+3, LineWidth=2, LineStyle=2)
plot.Set(gr_s2_300, LineColor=ROOT.kRed, MarkerColor=ROOT.kRed, LineWidth=2, LineStyle=2)

canv = ROOT.TCanvas('BTagEff','')
pads = plot.OnePad()
gr_s1_3000.GetYaxis().SetRangeUser(0,0.2)
gr_s1_3000.GetXaxis().SetRangeUser(0.8,1.2)
gr_s1_3000.GetXaxis().SetNdivisions(9)
gr_s1_3000.Draw('APL')
axishist = plot.GetAxisHist(pads[0])
axishist.SetMinimum(0)
plot.Set(axishist.GetXaxis(), Title='B-tagging efficiency wrt current')
plot.Set(axishist.GetYaxis(), Title='Expected uncertainty on #mu_{VHbb}')

gr_s1_3000.Draw('PLSAME')
gr_s2_3000.Draw('PLSAME')
gr_s1_300.Draw('PLSAME')
gr_s2_300.Draw('PLSAME')

legend = ROOT.TLegend(0.65, 0.7, 0.9, 0.93, '', 'NBNDC')
legend.AddEntry(gr_s1_3000, 'YR2018 S1 (3000 fb^{-1} )', 'L')
legend.AddEntry(gr_s2_3000, 'YR2018 S2 (3000 fb^{-1} )', 'L')
legend.AddEntry(gr_s1_300, 'YR2018 S1 (300 fb^{-1} )', 'L')
legend.AddEntry(gr_s2_300, 'YR2018 S2 (300 fb^{-1} )', 'L')
legend.Draw()

plot.DrawCMSLogo(pads[0],'CMS','Projection',11,0.045,0.03,1.0,'',1.0)
plot.DrawTitle(pads[0],'#sqrt{s} = 13 TeV',3)
canv.SaveAs('BTagEff_NoIncSigThFig.pdf')
canv.Print('BTagEff_NoIncSigThFig.png')

