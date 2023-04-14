import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import pickle
from coffea.lookup_tools.dense_lookup import dense_lookup

samples = [
        "DYJetsToLL_M-50_HT-100to200",
        "DYJetsToLL_M-50_HT-1200to2500",
        "DYJetsToLL_M-50_HT-200to400",
        "DYJetsToLL_M-50_HT-2500toInf",
        "DYJetsToLL_M-50_HT-400to600",
        "DYJetsToLL_M-50_HT-600to800",
        "DYJetsToLL_M-50_HT-800to1200",
        "ST_s-channel_4f_leptonDecays",
        "ST_t-channel_antitop_4f_InclusiveDecays",
        "ST_t-channel_antitop_5f_InclusiveDecays",
        "ST_t-channel_top_4f_InclusiveDecays",
        "ST_t-channel_top_5f_InclusiveDecays",
        "ST_tW_antitop_5f_inclusiveDecays",
        "ST_tW_top_5f_inclusiveDecays",
        "TTTo2L2Nu",
        "TTToHadronic",
        "TTToSemiLeptonic",
        "WJetsToLNu_HT-100To200",
        "WJetsToLNu_HT-1200To2500",
        "WJetsToLNu_HT-200To400",
        "WJetsToLNu_HT-2500ToInf",
        "WJetsToLNu_HT-400To600",
        "WJetsToLNu_HT-600To800",
        "WJetsToLNu_HT-800To1200",
        "WW",
        "WZ",
        "ZZ"
]
	
header = st.container()
eff = st.container()

with header:
	st.title("b-tagging efficiencies")

with eff:
	st.text("Select MC sample and Jet flavor")
	
	# user inputs
	dataset_, flavor_ = st.columns(2)
	dataset = dataset_.selectbox("MC Sample", options=samples)
	flavor = flavor_.selectbox("Jet flavor", options=["b-Jets", "c-Jets", "Light Jets"])
	flavor_map = {"Light Jets": 0, "c-Jets": 4, "b-Jets": 5}
	
	# compute efficiencies
	with open("eff_hist.pkl", "rb") as f: eff_hist = pickle.load(f)
	eff = eff_hist[{"dataset": dataset}]
	eff = eff[{"passWP": True}] / eff[{"passWP": sum}]
	efflookup = dense_lookup(eff.values(), [ax.edges for ax in eff.axes])
	efflookup._axes[-1] = np.array([0., 4., 5., 6.])
	
	# plot efficiencies
	fig, ax = plt.subplots()
	pts = np.linspace(20, 500, 20)
	etas = np.linspace(0, 2.5, 4)
	pt, eta = np.meshgrid(pts, etas)
	eff = efflookup(pt, eta, flavor_map[flavor])
	heatmap = ax.pcolormesh(pt, eta, eff, cmap="viridis")#, vmin=0, vmax=1)
	cbar = fig.colorbar(heatmap)
	cbar.set_label(f"{flavor} b-tagging Efficiency")
	ax.set(xlabel="$p_T$ [GeV]", ylabel="$|\eta|$", title=dataset)
	
	st.pyplot(fig)
