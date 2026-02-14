from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot

from sentence_transformers import SentenceTransformer

import joblib
import numpy as np

#**************  SIGNALS *****************
class RunnerSignals(QObject):

    status_good = pyqtSignal()

    embedder_return = pyqtSignal(dict)

    plot_reducer_return = pyqtSignal(list)
#**************  SIGNALS *****************

# >>> MODEL LOADER >>>
class ModelRunner(QObject):
    def __init__(self):
        super().__init__()

        #**************  SIGNALS *****************
        self.signals = RunnerSignals()

        self._STATUS_ = False
        
        self._PLOT_REDUCER = None

        self._EMBEDDER = None

#__________________________________________________________________________________________________________
    
    def loadEmbedder(self):

        self._EMBEDDER = SentenceTransformer("all-MiniLM-L6-v2")

    @pyqtSlot(str, str)
    def runEmbedder(self, prompt: str, response: str, norm=True, list=False):
        
        if not self._STATUS_:
            print("Skipping not ready")
            return

        p = self._EMBEDDER.encode(
            prompt,
            convert_to_numpy=True,
            normalize_embeddings=norm,
            show_progress_bar=False
        )

        r = self._EMBEDDER.encode(
            response,
            convert_to_numpy=True,
            normalize_embeddings=norm,
            show_progress_bar=False
        )

        res = {
                "prompt" : {
                    "content" : prompt,
                    "emb" : p.tolist()
                },
                "response" : {
                   "content" : response,
                    "emb" : r.tolist()
                }
               }

        self.signals.embedder_return.emit(res)

#__________________________________________________________________________________________________________

    def loadPlotReducer(self):

        self._PLOT_REDUCER = joblib.load("models/umap_reducer.joblib")

    @pyqtSlot(dict, dict)
    def runPlotReducer(self, prompt: dict, response: dict):

        if not self._STATUS_:
            print("Skipping not ready")
            return

        p = np.array(list(prompt["emb"])).reshape(1, -1)
        r = np.array(list(response["emb"])).reshape(1, -1)

        p_res = self._PLOT_REDUCER.transform(p)

        r_res = self._PLOT_REDUCER.transform(r)

        res = [
            {"role" : "User", "content": prompt["content"], "x": p_res[0,0], "y": p_res[0,1]},
            {"role" : "Assistant", "content": response["content"], "x": r_res[0,0], "y": r_res[0,1]},
        ]
    
        self.signals.plot_reducer_return.emit(res)

#__________________________________________________________________________________________________________
    @pyqtSlot()
    def loadModels(self):

        self.loadEmbedder()

        self.loadPlotReducer()

        self.signals.status_good.emit()

        self._STATUS_ = True


# <<< MODEL LOADER <<<