Feature: Obtener la versión


  Scenario: Get Version

    When Pido la version
    Then Obtengo el siguiente objeto
      | version |
      | 1.0     |
    And Obtengo el codigo de estado 200

